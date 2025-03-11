
import json

import matplotlib.pyplot as plt
import numpy as np

import pandas as pd
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D, Input
from tensorflow.keras.losses import BinaryCrossentropy
from tensorflow.keras.metrics import BinaryAccuracy
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

from tensorflow.keras.preprocessing.image import ImageDataGenerator

# DATASET LOADING #

data: dict
with open("data/uniface_encoded.json", "r") as file:
    data = json.load(file)

df: pd.DataFrame
if data:
    df = pd.DataFrame(data)






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

train_generator = train_datagen.flow_from_directory(
    'data/train',
    target_size=(256, 256),
    batch_size=16,
    class_mode='binary'
)

val_generator = val_datagen.flow_from_directory(
    'data/validation',
    target_size=(256, 256),
    batch_size=16,
    class_mode='binary'
)

# DATASET PROCESSING #

x_train = 0
y_train = 0

x_val = 0
y_val = 0

x_test = 0

# MODEL PREPARATION #
pretrained_model = VGG16(weights='imagenet',
              include_top=False,
              input_shape=(256, 256, 3))

pretrained_model.trainable = False

# technique to "stack" layers, starting with pretrain model's layers
inputs = Input(shape=(256, 256, 3))

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

history = model.fit_generator(
    train_generator,
    epochs=epochs,
    steps_per_epoch=(2000 // 16),
    validation_data=val_generator,
    validation_steps=(800 // 16),
    verbose=1
)

# val_loss, val_accuracy = model.evaluate(x_val, y_val, verbose=2)
# print(f'Validation Accuracy: {val_accuracy:.4f}')
# print(f'Validation Loss: {val_loss:.4f}')

def plot_validation(val_loss, val_acc):
    pass

