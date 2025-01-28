import configparser
import json
import sys

import requests

config = configparser.ConfigParser()
config.read('config.ini')

if not config.has_section('Model'):
    print("[-] Startup failed: 'config.ini' not found.")
    exit(1)

params = {
    'models' : 'genai',
    'api_user': config['Model']['user'],
    'api_secret': config['Model']['secret']
}

def check_media(path_to_file: str):
    files = { 'media': open(path_to_file, 'rb') }
    r = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)

    return json.loads(r.text)

def parse_check(output: dict[str], debug=False) -> (int, int):
    proc = {
        'score' : 0,
        'time' : -1,
        'error' : None
    }
    ret = {
        'code' : 0,
        'message' : "n/a",
        'from' : 'internal'
    }

    if "request" in output.keys():
        if debug:
            print(f"[*] Finished in {output['request']['timestamp']}.")
        proc['time'] = output['request']['timestamp']


    if "status" in output.keys():
        if output['status'] == "success":
            ai_score = output['type']['ai_generated']

            if debug:
                print(f"[+] '{output['media']['uri']}' ai report: {"likely generated" if ai_score > 0.5 else "not generated"} with {ai_score * 100}% confidence.")

            proc['score'] = ai_score

        elif output['status'] == "failure":
            error_code = output['error']['code']
            error_msg = output['error']['message']

            if debug:
                print(f"[-] {output['error']['type'].upper()} with return code {error_code}: {output['error']['message']}.")

            ret['code'] = error_code
            ret['message'] = error_msg
            ret['from'] = 'sightengine'
        else:
            print(output)

    proc['error'] = ret
    return proc


if __name__ == "__main__":

    if len(sys.argv) > 1:
        print(parse_check(check_media(sys.argv[1]), True))
    # else:
    #     print(parse_check(check_media("./img.jpg"), True))

""" RESPONSE EXAMPLE
{
    "status": "success",
    "request": {
        "id": "req_0zrbHDeitGYY7wEGncAne",
        "timestamp": 1491402308.4762,
        "operations": 1
    },
    "type": {
      "ai_generated": 0.01
    },
    "media": {
        "id": "med_0zrbk8nlp4vwI5WxIqQ4u",
        "uri": "https://sightengine.com/assets/img/examples/example-prop-c2.jpg"
    }
}
"""
