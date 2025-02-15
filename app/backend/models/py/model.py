import configparser
import json
import sys
from datetime import datetime

import db

import requests

from result import Result

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

# NOTE(liam): JUST PLACEHOLDER EXPLANATION
explanations = {
    "ok" : [
        "Looks good.",
        "No artifacts found.",
        "Likely nothing.",
        "The video exhibits natural facial movements consistent with the speaker's emotions.",
        "The lighting and shadows on the face align with the surrounding environment.",
        "The background looks realistic and properly aligned with the subject.",
        "The subject's eye movements and blinking are natural and consistent.",
        "The speech and lip-syncing match perfectly, with no delays or inconsistencies.",
        "The skin tone and texture of the face are consistent with the rest of the body.",
        "The video resolution is stable throughout and shows no noticeable glitches.",
        "There are no visible artifacts or distortions in the video frames.",
        "The transitions between different facial expressions are smooth and realistic.",
        "The voice matches the speaker's facial expressions and body movements.",
        "The hair movement is natural and consistent with real-life physics.",
        "There is no odd distortion around the subject's face or body.",
        "The audio is crisp and clear, with no glitches or interruptions.",
        "The person's gaze follows the natural flow of the scene without inconsistency.",
        "The subject's head and body movements appear realistic and not overly stiff.",
        "There is no visible pixelation, distortion, or artifacts around the subject.",
        "The shadows on the face align properly with the lighting in the environment.",
        "There are no noticeable inconsistencies in the reflection or details of the face.",
        "The subject's body language matches the tone and content of the speech.",
        "There are no unnatural smoothness or over-polishing of the skin on the face.",
        "The audio track is perfectly synchronized with the movements of the speaker’s mouth.",
        "The subject's expressions transition fluidly and naturally from one to the next.",
        "The video resolution remains consistent across all frames and angles.",
        "The subject’s face shows natural wrinkles, pores, and skin texture.",
        "The background environment looks realistic, without visible signs of manipulation.",
        "The person’s head size and proportion appear natural in relation to their body.",
        "The voice is distinct and matches the speaker’s physical presence and movements.",
        "The video does not contain any abrupt transitions or glitches during playback.",
        "The lighting on the subject’s face follows the natural flow of the scene.",
        "The person's movements match their speech in a fluid, believable way.",
        "The eyes and face show subtle expressions that convey emotion naturally.",
        "There are no discrepancies in how the subject's face interacts with the environment.",
        "The video maintains a consistent frame rate with no noticeable jumps or delays.",
        "The subject’s clothing, hair, and facial features appear natural and consistent.",
        "The subject’s mouth movements align properly with the sounds being made.",
        "The background remains stable and coherent throughout the video.",
        "The voice matches the person’s age, gender, and other vocal characteristics.",
        "The transitions between scenes are smooth, with no awkward cuts or distortions.",
        "The video contains natural shadows that blend seamlessly with the subject’s face.",
        "There are no noticeable differences in color or texture between the subject’s face and the rest of their body.",
        "The subject’s facial expressions align perfectly with the tone and content of their speech.",
        "There are no inconsistencies in the subject’s movements relative to their surroundings.",
        "The video maintains consistent resolution and sharpness throughout.",
        "The subject's eyes blink naturally and follow the flow of the scene.",
        "The person’s facial features are symmetrical and properly proportioned.",
        "The voice is clear and matches the physical movement of the speaker’s mouth.",
        "The subject’s movements are fluid and natural, with no jerky or mechanical motions.",
        "The face maintains a consistent level of detail throughout the video.",
        "There is no noticeable lag or out-of-sync audio during speech.",
        "The subject's gaze seems to match the direction of their speech or surroundings.",
        "The video quality is stable, with no sudden drops in clarity or detail.",
        "The subject's mouth movements match the words being spoken without delay.",
        "The subject’s eyes maintain proper gaze direction and appear natural in their motion.",
        "There is no odd flickering or distortion in the video frames.",
        "The subject’s face and body movements appear consistent with normal human behavior.",
        "There is no unnatural smoothness to the skin on the face or body.",
        "The lighting and shadows in the video behave realistically according to the environment.",
        "The background does not show signs of manipulation or artificiality.",
        "The audio is synced with the person’s mouth and facial expressions perfectly.",
        "There are no artifacts or glitches disrupting the video’s visual consistency.",
        "The person’s body language aligns with their speech and overall demeanor.",
        "The facial expressions match the spoken words and are not exaggerated or out of place.",
        "The subject's hands and arms move naturally, with no stiff or unnatural motions.",
        "The background setting remains consistent and believable throughout the video.",
        "The subject’s posture and body movements look natural and unforced.",
        "The subject’s face displays natural aging signs like wrinkles and facial lines.",
        "There is no distortion or strange blurring around the edges of the person’s face.",
        "The video shows no signs of compression or unnatural pixelation.",
        "The subject’s movements are in sync with the environment around them.",
        "The subject's eyes appear focused and blink at natural intervals.",
        "The audio and video remain in sync throughout the entire clip.",
        "There are no signs of audio distortion or robotic-sounding voices.",
        "The subject’s face and features look realistic and human-like.",
        "The lighting on the subject’s face interacts with the environment correctly.",
        "The background is sharp and clear, with no evidence of manipulation.",
        "The video is stable and free of interruptions or distortions.",
        "There is a natural flow in the subject’s facial expressions during the speech.",
        "The subject’s gestures and body language appear authentic and not computer-generated.",
        "The skin tone on the face matches that of the subject’s neck and hands.",
        "The subject’s facial expressions align perfectly with the content of the dialogue.",
        "The subject’s head moves naturally in sync with the rest of their body.",
        "There is no distortion or artifacts in the background or surroundings.",
        "The subject’s eyes and mouth match their movements with their spoken words.",
        "The facial expressions smoothly transition from one to the next, showing emotional continuity.",
        "The subject’s posture remains consistent and comfortable throughout.",
        "The subject’s movements in the video are believable and typical of real-life behavior.",
        "The background environment complements the subject’s actions and speech.",
        "The subject’s mouth articulates the words naturally, without robotic movement.",
        "The lighting in the video remains consistent with the natural environment.",
        "The subject’s face shows natural aging and facial texture, not overly smoothed or airbrushed.",
        "There is no inconsistent pixelation or unusual blurring in the video.",
        "The subject’s body proportions and head size are typical and realistic.",
        "The facial features are detailed and resemble a real human face in their movements.",
        "The video maintains a consistent quality with no sudden drops in visual detail.",
        "The voice has natural variation and emotion, not flat or computer-generated.",
        "There are no unusual or forced movements in the subject’s body or face.",
        "The background consistently matches the subject’s actions and environment.",
        "The audio track is clean and devoid of noticeable robotic effects.",
        "The subject’s gestures and body language appear realistic and relatable.",
        "The lighting on the face and background blends seamlessly throughout the video.",
        "The subject’s face and voice align with their physical characteristics and actions.",
        "The subject’s mouth moves in sync with the speech without unnatural delays or jumps.",
        "The video quality stays consistent and stable without sudden distortions.",
        "The subject’s voice and facial expressions match the context and tone of the scene.",
        "The background and setting are coherent and believable within the scene."
        ],
    "gen" : [
        "Artifacts found in certain regions.",
        "Even a baby could tell it's generated.",
        "Something's not right with that image.",
        "The image exhibits unnatural facial movements.",
        "There are inconsistencies in the lighting on the face.",
        "The video has strange artifacts around the edges.",
        "The subject's eyes are not blinking in a natural way.",
        "The lip-syncing doesn't match the speech accurately.",
        "There is an odd distortion around the subject's face.",
        "The shadows don't align with the light source.",
        "The background appears inconsistent with the foreground.",
        "The subject's skin texture looks unusually smooth.",
        "There are visible glitches in the video frame.",
        "The transition between facial expressions is too abrupt.",
        "The video has unnatural blurring or pixelation.",
        "The person’s voice doesn't match the facial movements.",
        "The subject's hair has unrealistic motion or detail.",
        "The video contains awkward facial expressions that seem off.",
        "The lighting doesn't match the overall scene lighting.",
        "The eyes seem to be unnaturally fixed or too wide.",
        "There’s an odd glow around the edges of the person’s face.",
        "The audio seems to be out of sync with the video.",
        "The background environment appears unnatural or computer-generated.",
        "There are visible inconsistencies with the person's shadow.",
        "The person's gaze seems to be disconnected from the scene.",
        "There are noticeable distortions when the person moves.",
        "The subject’s movements look stiff or unnatural.",
        "The video contains pixel-level glitches that are hard to ignore.",
        "The face lacks natural wrinkles and other aging features.",
        "There’s a noticeable mismatch between the voice and the mouth movements.",
        "The skin tone of the face is not consistent with the rest of the body.",
        "The subject's pupils seem unnaturally dilated or fixed.",
        "The facial features appear poorly rendered or over-simplified.",
        "There’s an inconsistent or unnatural reflection on the person's face.",
        "The voice sounds muffled or robotic in certain parts of the video.",
        "The face appears distorted when moving in certain angles.",
        "There are visible seams or edges where the face was altered.",
        "The video has unnatural smoothness or a lack of detail in certain parts.",
        "The subject’s eyes appear to be looking in two different directions.",
        "The person's mouth moves without proper articulation.",
        "The face lacks natural skin texture or depth.",
        "There’s a noticeable unnatural color shift in certain parts of the image.",
        "The audio track seems to jump or glitch at times.",
        "The person’s facial expressions seem out of sync with the scene.",
        "The video resolution changes abruptly in certain areas.",
        "There are unnatural patterns in the subject’s clothing or hair.",
        "The subject’s head movement seems too jerky or robotic.",
        "The face looks too perfect and lacks natural imperfections.",
        "The motion of the subject’s mouth doesn’t align with the words spoken.",
        "The facial features lack depth or shadows.",
        "The subject’s ears are not visible or look artificial.",
        "There’s an uncanny smoothness to the subject's face.",
        "The body movements of the subject seem too fluid or exaggerated.",
        "The subject’s face looks overly polished and unrealistic.",
        "There is strange lighting or reflection on the face.",
        "The eyes lack the natural variation in gaze direction.",
        "The subject’s voice doesn’t match their body language.",
        "The subject’s head appears disproportionately large or small.",
        "The lips do not sync up with the sounds being made.",
        "The clothing patterns are strangely inconsistent in the video.",
        "The subject's face exhibits unnatural blinking behavior.",
        "There are visible unnatural transitions between different scenes.",
        "The video shows noticeable distortion at the edges of the face.",
        "The voice seems disjointed or disconnected from the speaker's movements.",
        "The lighting and shadows do not behave realistically on the subject’s face.",
        "The person's mouth doesn’t move in a natural way during speech.",
        "The subject’s hands seem unnaturally stiff or out of place.",
        "The subject’s body movements appear disjointed or awkward.",
        "There are inconsistent textures on the person's face or skin.",
        "The facial expressions do not transition smoothly from one to the next.",
        "There’s a delay between the person's mouth movements and the voice.",
        "The background changes unexpectedly or doesn’t match the subject’s movements.",
        "There’s noticeable pixelation or distortion on the subject’s face.",
        "The subject’s voice pitch fluctuates unnaturally during speech.",
        "The subject’s face shows an unnatural or constant expression.",
        "There are visible lines or marks around the person’s face.",
        "The video seems unnaturally crisp or too sharp in certain areas.",
        "The subject's mouth movements seem out of place with the words spoken.",
        "There are irregular lighting effects around the subject's face.",
        "The subject’s body appears too rigid or unnatural in the video.",
        "There are sudden, jarring changes in the video quality.",
        "The video shows clear signs of distortion or compression.",
        "The subject’s mouth doesn’t properly articulate the speech sounds.",
        "The subject’s movements appear sped up or slowed down unnaturally.",
        "The subject’s body doesn't match the surrounding environment in size.",
        "The subject’s skin looks overly smooth or waxy.",
        "The video has noticeable lag or delay during movement.",
        "The subject's movements are jerky or disjointed during transitions.",
        "The subject’s eyes don't blink naturally or appear frozen.",
        "There are strange edges around the subject’s face or hair.",
        "The audio is distorted or seems robotic at times.",
        "There are sharp contrasts between the person's features and their surroundings.",
        "The lighting on the face seems unnatural or inconsistent.",
        "There is an abnormal gap between the subject's mouth and the sounds.",
        "The subject’s body looks unnatural in certain poses.",
        "The subject's features appear to have been artificially altered.",
        "The facial expressions are too exaggerated or unnatural.",
        "The person’s voice is too perfect or too mechanical.",
        "The subject’s mouth movements don’t match the surrounding environment.",
        "There are visible inconsistencies with the shadows and reflections.",
        "The subject’s facial features look oddly proportioned.",
        "The background lighting changes unexpectedly during the video.",
        "The subject’s eyes are over-exaggerated or unnaturally large.",
        "The video is grainy or pixelated in certain areas.",
        "There are unnatural pauses or breaks in the speech or audio.",
        "The subject’s hands appear too blurry or misshapen.",
        "The face exhibits unnatural symmetry that is not typical for humans.",
        "The voice sounds computer-generated or synthetic at times.",
        "The subject's eyes appear to move in a robotic, unnatural manner.",
        "The video features strange stretching of the subject's facial features.",
        "The background is blurry or inconsistent with the scene.",
        "There are inconsistencies in the lighting when the subject moves.",
        "The subject’s body language doesn’t match their tone of voice.",
        "There is excessive sharpness in some parts of the image.",
        "The video seems unnaturally polished or overly edited."
        ]
}

def generate_explanation(was_generated: bool = True) -> str:
    res = ""
    def to_integer(dt_time):
        return 10000*dt_time.year + 100*dt_time.month + dt_time.day + dt_time.second
    if was_generated:
        res = explanations["gen"][to_integer(datetime.now()) % len(explanations["gen"])]
    else:
        res = explanations["ok"][to_integer(datetime.now()) % len(explanations["ok"])]

    return res


def check_media(path_to_file: str):
    files = { 'media': open(path_to_file, 'rb') }
    r = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)

    res = json.loads(r.text)
    print(res)

    return res

def parse_check(output: dict[str], debug=False) -> (int, int):
    proc = {
        'score' : 0,
        'time' : -1,
        'error' : None, # ret is passed here.
        'model' : { 'name': params['models'], 'version': '1.0' },
        'expl' : "n/a"
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
            proc['expl'] = generate_explanation(was_generated=True if ai_score > 0.5 else False)


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


def push_results(sess, res, hash):
    newResult = Result(hash, res['time'], res['score'], res['expl'], res['error']['from'], res['error']['code'])
    sess.add(newResult)
    sess.commit()

if __name__ == "__main__":

    # NOTE(liam): for debugging.
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
