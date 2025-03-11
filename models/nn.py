
import json
import os

import matplotlib.pyplot as plt
import numpy as np

import pandas as pd
from tensorflow.keras.applications import VGG16
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D, Input
from tensorflow.keras.losses import BinaryCrossentropy
from tensorflow.keras.metrics import BinaryAccuracy
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.train import latest_checkpoint

# constants #

model_name = "vgg16"

data_dir = "data"
img_size = 256 # assume same for both width and height

# assume there is a json file of the same name inside these data subdirs.
data_user_dir = f"{data_dir}/user"
data_uniface_dir = f"{data_dir}/uniface"

checkpoint_dir = "checkpoints"
checkpoint_path = f"{checkpoint_dir}/{model_name}/" + "cp-{epoch:04d}.ckpt"
batch_size = 16

# DATASET LOADING #

def data_load(path_to_json: str) -> pd.DataFrame:
    data: dict = {}
    df: pd.DataFrame = None

    with open(path_to_json, "r") as file:
        data = json.load(file)

    if data:
        df = pd.DataFrame(data)

    return df

frames = [
    data_load(f"{data_user_dir}/user.json"),
    data_load(f"{data_uniface_dir}/uniface.json"),
]

# TODO(liam): this definitely won't work as is.
df = pd.concat(frames)

# DATASET PROCESSING #

train_datagen = ImageDataGenerator(
    rescale=(1./255),
    zoom_range=0.2,
    horizontal_flip=True,
    vertical_flip=True,
    brightness_range=[-0.5, 0.5],
    rotation_range=0.2,
    shear_range=0.2,
    fill_mode='nearest'
)
val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_dataframe(
    df,
    x_col = "filename",
    y_col = "label",
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode='binary',
    validate_filenames=True
)
val_generator = val_datagen.flow_from_dataframe(
    df,
    x_col = "filename",
    y_col = "label",
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode='binary',
    validate_filenames=True
)

# MODEL PREPARATION #

pretrained_model = VGG16(
    weights='imagenet',
    include_top=False,
    input_shape=(img_size, img_size, 3)
)

pretrained_model.trainable = False

# technique to "stack" layers, starting with pretrain model's layers
inputs = Input(shape=(img_size, img_size, 3))

cl = pretrained_model(inputs, training=False)

cl = GlobalAveragePooling2D()(cl)
cl = Dropout(0.2)(cl)
# cl = Dense(512, activation='relu')(cl)

# this is the final layer; size must equal desired output size
outputs = Dense(2, activation='softmax')(cl)
model = Model(inputs, outputs)

model.summary(show_trainable=True)

# hyperparameters
epochs = 10
learning_rate = 1e-6

# pretrained_model.trainable = True
# model.summary(show_trainable=True)

model.compile(
    optimizer=Adam(learning_rate),
    loss=BinaryCrossentropy(from_logits=True),
    metrics=[BinaryAccuracy()]
)

# MODEL TRAINING #

checkpoint_callback = ModelCheckpoint(
    filepath=os.path.join(os.getcwd(), checkpoint_dir, checkpoint_path),
    save_weights_only=True,
    save_freq=5 * batch_size,
    verbose=1
)

latest = latest_checkpoint(os.path.join(os.path(os.getcwd(), checkpoint_dir)))
model.load_weights(latest)

history = model.fit_generator(
    train_generator,
    epochs=epochs,
    steps_per_epoch=(2000 // 16),
    validation_data=val_generator,
    validation_steps=(800 // 16),
    callback=[checkpoint_callback],
    verbose=1
)

# val_loss, val_accuracy = model.evaluate(x_val, y_val, verbose=2)
# print(f'Validation Accuracy: {val_accuracy:.4f}')
# print(f'Validation Loss: {val_loss:.4f}')

def plot_validation(val_loss, val_acc):
    pass

def model_save(model, name, version):
    model.save(f"deepfake-{name}-{version}.keras")

