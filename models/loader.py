
import logging
import os
import sys

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

import numpy as np
from tensorflow.keras.config import disable_interactive_logging
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

log_dir: str = "log"
model_output_dir: str = "models/output"
model_error_message: str = ""
img_size = 256


# logging
disable_interactive_logging()
log = logging.getLogger('tensorflow')
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh = logging.FileHandler(os.path.join(os.getcwd(), log_dir, 'tensorflow.log'))
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
log.addHandler(fh)

def model_generate_prediction(image_path: str, model_name: str = 'vgg16'):
    global model_error_message
    fullname = f"deepfake-{model_name}.keras"

    prediction = 0
    error_code = 0

    try:
        x = image.load_img(image_path, target_size=(img_size, img_size))
        x_arr = image.img_to_array(x)
        x_arr = np.expand_dims(x_arr, axis=0)
        x_in = np.vstack([x_arr])

        model = load_model(os.path.join(os.getcwd(), model_output_dir, fullname))
        model.compile(optimizer='adam',
                      loss='binary_crossentropy',
                      metrics=['accuracy'])

        prediction = model.predict(x_in)
        prediction = round(prediction[0][0].astype(float), 3).item()
    except Exception as e:
        model_error_message = e
        error_code = 1

    return prediction, error_code

def model_get_error() -> str:
    global model_error_message

    result = model_error_message
    model_error_message = ""

    return result

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print("prediction:", model_generate_prediction(sys.argv[1]))
