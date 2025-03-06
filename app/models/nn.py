
import matplotlib.pyplot as plt
import numpy as np

import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model

# DATASET PROCESSING HERE #

x_train = 0
y_train = 0

x_val = 0
y_val = 0

x_test = 0

# MODEL #
pretrained_model = VGG16(weights='imagenet',
              include_top=False,
              input_shape=(32, 32, 3))

# technique to "stack" layers, starting with pretrain model's layers
cl = pretrained_model.output

# this part can be changed
cl = GlobalAveragePooling2D()(cl)
cl = Dense(512, activation='relu')(cl)

# this is the final layer; size must equal desired output size
predictions = Dense(2, activation='softmax')(cl)
model = Model(inputs=pretrained_model.input, outputs=predictions)

# initially freeze the pretrained model's layers
for layer in pretrained_model.layers:
    layer.trainable = False

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

for layer in model.layers[-4:]:
    layer.trainable = True

# hyperparameters
eps = 10

history = model.fit(x_train, y_train, epochs=eps,
                    validation_data=(x_val, y_val),
                    verbose=1)

# val_loss, val_accuracy = model.evaluate(x_val, y_val, verbose=2)
# print(f'Validation Accuracy: {val_accuracy:.4f}')
# print(f'Validation Loss: {val_loss:.4f}')

def plot_validation(val_loss, val_acc):
    pass



