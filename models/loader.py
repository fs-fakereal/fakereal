
import os
import sys

import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

def model_generate_prediction(image_path: str, model_name: str = 'vgg16'):
    fullname = f"deepfake-{model_name}.keras"
    prediction = 0

    try:
        x = image.load_img(image_path)
        x_arr = image.img_to_array(x)
        x_arr = np.expand_dims(x_arr, axis=0)
        x_in = np.vstack([x_arr])

        model = load_model(os.path.join(os.getcwd(), 'shelf', fullname))
        model.compile(optimizer='adam',
                      loss='binary_crossentropy',
                      metrics=['accuracy'])

        prediction = model.predict(x_in)
        prediction = prediction[0][0]
    except Exception as e:
        print(e)

    return prediction

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print("prediction: ", 'true' if np.round(model_generate_prediction(sys.argv[1])) == 1 else 'false')
