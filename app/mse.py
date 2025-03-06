import json
import os
from datetime import datetime

import requests
from app.result import Result

default_model_api_params = {
    'models' : 'genai',
    'user': os.getenv('MODEL_USER'),
    'secret': os.getenv('MODEL_SECRET')
}

explanations = {
    "ok" : [
        "Looks good.",
        "No artifacts found.",
        "Likely nothing.",
        "The background looks realistic and properly aligned with the subject.",
        "No delays or inconsistencies found.",
        "There are no visible artifacts or distortions.",
        "There is no odd distortion around the subject's face or body.",
        "The person's gaze follows the natural flow of the scene without inconsistency.",
        "The subject's head and body movements appear realistic and not overly stiff.",
        "There is no visible pixelation, distortion, or artifacts around the subject.",
        "The shadows on the face align properly with the lighting in the environment.",
        "There are no noticeable inconsistencies in the reflection or details of the face.",
        "The subject's body language matches the tone and content of the speech.",
        "There are no unnatural smoothness or over-polishing of the skin on the face.",
        "The subject's expressions transition fluidly and naturally from one to the next.",
        "The subject’s face shows natural wrinkles, pores, and skin texture.",
        "The background environment looks realistic, without visible signs of manipulation.",
        "The person’s head size and proportion appear natural in relation to their body.",
        "The lighting on the subject’s face follows the natural flow of the scene.",
        "The person's movements match their speech in a fluid, believable way.",
        "The eyes and face show subtle expressions that convey emotion naturally.",
        "There are no discrepancies in how the subject's face interacts with the environment.",
        "The subject’s clothing, hair, and facial features appear natural and consistent.",
        "The subject’s mouth movements align properly with the sounds being made.",
        "The transitions between scenes are smooth, with no awkward cuts or distortions.",
        "There are no noticeable differences in color or texture between the subject’s face and the rest of their body.",
        "The subject’s facial expressions align perfectly with the tone and content of their speech.",
        "There are no inconsistencies in the subject’s movements relative to their surroundings.",
        "The subject's eyes blink naturally and follow the flow of the scene.",
        "The person’s facial features are symmetrical and properly proportioned.",
        "The subject’s movements are fluid and natural, with no jerky or mechanical motions.",
        "The subject's gaze seems to match the direction of their speech or surroundings.",
        "The subject's mouth movements match the words being spoken without delay.",
        "The subject’s eyes maintain proper gaze direction and appear natural in their motion.",
        "The subject’s face and body movements appear consistent with normal human behavior.",
        "There is no unnatural smoothness to the skin on the face or body.",
        "The background does not show signs of manipulation or artificiality.",
        "The person’s body language aligns with their speech and overall demeanor.",
        "The facial expressions match the spoken words and are not exaggerated or out of place.",
        "The subject's hands and arms move naturally, with no stiff or unnatural motions.",
        "The subject’s posture and body movements look natural and unforced.",
        "The subject’s face displays natural aging signs like wrinkles and facial lines.",
        "There is no distortion or strange blurring around the edges of the person’s face.",
        "The subject’s movements are in sync with the environment around them.",
        "The subject's eyes appear focused and blink at natural intervals.",
        "The subject’s face and features look realistic and human-like.",
        "The lighting on the subject’s face interacts with the environment correctly.",
        "The background is sharp and clear, with no evidence of manipulation.",
        "The subject’s gestures and body language appear authentic and not computer-generated.",
        "The skin tone on the face matches that of the subject’s neck and hands.",
        "The subject’s facial expressions align perfectly with the content of the dialogue.",
        "The subject’s head moves naturally in sync with the rest of their body.",
        "There is no distortion or artifacts in the background or surroundings.",
        "The subject’s eyes and mouth match their movements with their spoken words.",
        "The facial expressions smoothly transition from one to the next, showing emotional continuity.",
        "The subject’s posture remains consistent and comfortable throughout.",
        "The background environment complements the subject’s actions and speech.",
        "The subject’s mouth articulates the words naturally, without robotic movement.",
        "The subject’s face shows natural aging and facial texture, not overly smoothed or airbrushed.",
        "The subject’s body proportions and head size are typical and realistic.",
        "The facial features are detailed and resemble a real human face in their movements.",
        "There are no unusual or forced movements in the subject’s body or face.",
        "The background consistently matches the subject’s actions and environment.",
        "The subject’s gestures and body language appear realistic and relatable.",
        "The subject’s mouth moves in sync with the speech without unnatural delays or jumps.",
        "The background and setting are coherent and believable within the scene."
        ],
    "gen" : [
        "Artifacts found in certain regions.",
        "Even a baby could tell it's generated.",
        "Something's not right with that image.",
        "The image exhibits unnatural facial movements.",
        "There are inconsistencies in the lighting on the face.",
        "The subject's eyes are not blinking in a natural way.",
        "The lip-syncing doesn't match the speech accurately.",
        "There is an odd distortion around the subject's face.",
        "The shadows don't align with the light source.",
        "The background appears inconsistent with the foreground.",
        "The subject's skin texture looks unusually smooth.",
        "The transition between facial expressions is too abrupt.",
        "The subject's hair has unrealistic motion or detail.",
        "The lighting doesn't match the overall scene lighting.",
        "The eyes seem to be unnaturally fixed or too wide.",
        "There’s an odd glow around the edges of the person’s face.",
        "The background environment appears unnatural or computer-generated.",
        "There are visible inconsistencies with the person's shadow.",
        "The person's gaze seems to be disconnected from the scene.",
        "There are noticeable distortions when the person moves.",
        "The subject’s movements look stiff or unnatural.",
        "The face lacks natural wrinkles and other aging features.",
        "The skin tone of the face is not consistent with the rest of the body.",
        "The subject's pupils seem unnaturally dilated or fixed.",
        "The facial features appear poorly rendered or over-simplified.",
        "There’s an inconsistent or unnatural reflection on the person's face.",
        "The face appears distorted when moving in certain angles.",
        "There are visible seams or edges where the face was altered.",
        "The subject’s eyes appear to be looking in two different directions.",
        "The person's mouth moves without proper articulation.",
        "The face lacks natural skin texture or depth.",
        "There’s a noticeable unnatural color shift in certain parts of the image.",
        "The person’s facial expressions seem out of sync with the scene.",
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
        "The subject’s head appears disproportionately large or small.",
        "The lips do not sync up with the sounds being made.",
        "The subject's face exhibits unnatural blinking behavior.",
        "There are visible unnatural transitions between different scenes.",
        "The lighting and shadows do not behave realistically on the subject’s face.",
        "The person's mouth doesn’t move in a natural way during speech.",
        "The subject’s hands seem unnaturally stiff or out of place.",
        "The subject’s body movements appear disjointed or awkward.",
        "There are inconsistent textures on the person's face or skin.",
        "The facial expressions do not transition smoothly from one to the next.",
        "The background changes unexpectedly or doesn’t match the subject’s movements.",
        "There’s noticeable pixelation or distortion on the subject’s face.",
        "The subject’s face shows an unnatural or constant expression.",
        "There are visible lines or marks around the person’s face.",
        "The subject's mouth movements seem out of place with the words spoken.",
        "There are irregular lighting effects around the subject's face.",
        "The subject’s mouth doesn’t properly articulate the speech sounds.",
        "The subject’s movements appear sped up or slowed down unnaturally.",
        "The subject’s body doesn't match the surrounding environment in size.",
        "The subject’s skin looks overly smooth or waxy.",
        "The subject's movements are jerky or disjointed during transitions.",
        "The subject’s eyes don't blink naturally or appear frozen.",
        "There are strange edges around the subject’s face or hair.",
        "There are sharp contrasts between the person's features and their surroundings.",
        "The lighting on the face seems unnatural or inconsistent.",
        "There is an abnormal gap between the subject's mouth and the sounds.",
        "The subject’s body looks unnatural in certain poses.",
        "The subject's features appear to have been artificially altered.",
        "The facial expressions are too exaggerated or unnatural.",
        "The subject’s mouth movements don’t match the surrounding environment.",
        "There are visible inconsistencies with the shadows and reflections.",
        "The subject’s facial features look oddly proportioned.",
        "The subject’s eyes are over-exaggerated or unnaturally large.",
        "The subject’s hands appear too blurry or misshapen.",
        "The face exhibits unnatural symmetry that is not typical for humans.",
        "The subject's eyes appear to move in a robotic, unnatural manner.",
        "The background is blurry or inconsistent with the scene.",
        "There are inconsistencies in the lighting when the subject moves.",
        "There is excessive sharpness in some parts of the image.",
        ]
}

# NOTE(liam): JUST PLACEHOLDER EXPLANATION

def file_get_extension(filename):
    return filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''


def generate_explanation(was_generated: bool = True) -> str:
    res = ""
    def to_integer(dt_time):
        return 10000*dt_time.year + 100*dt_time.month + dt_time.day + dt_time.second
    if was_generated:
        res = explanations["gen"][to_integer(datetime.now()) % len(explanations["gen"])]
    else:
        res = explanations["ok"][to_integer(datetime.now()) % len(explanations["ok"])]

    return res

def push_results(sess, res, hash):
    # TODO(liam): currently failing
    newResult = Result(hash, res['time'], res['score'], res['expl'], res['error']['from'], res['error']['code'])
    sess.add(newResult)
    sess.commit()

#-------- new functions --------#

def prediction(path: str, args: dict) -> dict:
    if "model_id" not in args.keys():
        raise ValueError("Missing model_id argument")

    result: dict = {}

    if args['model_id'] in ['inception', 'resnet', 'vgg16']:
        if "prefer" not in args.keys():
            raise ValueError("Missing prefer argument")
        pass
    else:
        if "user" not in args.keys() and "secret" not in args.keys():
            result = call_api_and_predict(path)
        else:
            result = call_api_and_predict(path, args)

    return result

def call_api_and_predict(path : str, args : dict = default_model_api_params, debug : bool = False) -> dict:
    result = {
        'score' : 0,
        'time' : -1,
        'status' : None, # status is passed here.
        'model' : None,
        'explanation' : "n/a"
    }
    status = {
        'code' : 0,
        'message' : "n/a",
        'from' : 'internal'
    }
    model = {
        'name' : args['models'] if 'models' in args.keys() else args['model_id'],
        'version' : '1.0'
    }

    # REQUEST
    files = { 'media' : open(path, 'rb') }

    req_json = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data={
        'models' : model['name'],
        'api_user' : args['user'],
        'api_secret' : args['secret']
    })

    res = json.loads(req_json.text)

    # PARSING
    if "request" in res.keys():
        if debug:
            print(f"[*] Finished in {res['request']['timestamp']}.")
        result['time'] = res['request']['timestamp']


    if "status" in res.keys():
        if res['status'] == "success":
            ai_score = res['type']['ai_generated']

            if debug:
                print(f"[+] '{result['media']['uri']}' ai report: {"likely generated" if ai_score > 0.5 else "not generated"} with {ai_score * 100}% confidence.")

            result['score'] = ai_score
            result['explanation'] = generate_explanation(was_generated=True if ai_score > 0.5 else False)


        elif result['status'] == "failure":
            error_code = res['error']['code']
            error_msg = res['error']['message']

            if debug:
                print(f"[-] {result['error']['type'].upper()} with status code {error_code}: {result['error']['message']}.")

            status['code'] = error_code
            status['message'] = error_msg
            status['from'] = 'sightengine'
        else:
            print(result)

    result['status'] = status
    result['model'] = model
    return result


def load_model_and_predict(path, args) -> dict:
    result = {
        'score' : 0,
        'time' : -1,
        'status' : None, # status is passed here.
        'model' : None,
        'explanation' : "n/a"
    }
    status = {
        'code' : 0,
        'message' : "n/a",
        'from' : 'internal'
    }
    model = {
        'name' : args['model_id'],
        'version' : ""
    }
    # TODO(liam): add code here



    result['status'] = status
    result['model'] = model
    return result

