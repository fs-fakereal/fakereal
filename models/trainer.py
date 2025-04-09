
import json
import os

import matplotlib.pyplot as plt
import numpy as np

import pandas as pd
from tensorflow.keras.applications import MobileNetV3Small, VGG16
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D, Input
from tensorflow.keras.losses import BinaryCrossentropy
from tensorflow.keras.metrics import BinaryAccuracy
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.train import latest_checkpoint

### constants ###

# LIKELY ONLY CHANGE THESE PARAMETERS #
# ----------------------------------- #
model_pretrained = MobileNetV3Small
model_name = "mobilenetv3small"
dataset_name = "uniface-ff"

# hyperparameters #
epochs = 10
learning_rate = 1e-6
batch_size = 16
# ----------------------------------- #

# -------------- FIXED -------------- #
img_size = 256 # assume same for both width and height
data_dir = "data"
output_dir = "output"
# assume there is a json file of the same name inside these data subdirs.
checkpoint_dir = "checkpoints"
checkpoint_path = f"{checkpoint_dir}/{model_name}/" + "cp-{epoch:04d}.ckpt"
# ----------------------------------- #

# ------------ FUNCTIONS ------------ #
def dataLoad(dataset_name: str) -> (pd.DataFrame, pd.DataFrame, ImageDataGenerator, ImageDataGenerator):
    # DATASET LOADING #
    # overall path of uniface dataset:
    # - DF40_train/uniface/ff/frames                    |> primarily here
    # - DF40/uniface/ff/frames
    # - FaceForensics++/original_sequences/youtube/c23


    # TODO(liam): it could be possible that this is deallocated
    # when the function finished, causing an error with the data
    # generator.
    df_train: pd.DataFrame = pd.read_csv(f"{data_dir}/{dataset_name}-train.csv")
    df_val: pd.DataFrame = pd.read_csv(f"{data_dir}/{dataset_name}-test.csv")

    df_train['label'] = df_train['label'].astype('str')
    df_val['label'] = df_val['label'].astype('str')

    # DATASET PROCESSING #
    train_datagen = ImageDataGenerator(
        rescale=(1./255),
        zoom_range=[0.5, 1.5],
        horizontal_flip=True,
        vertical_flip=True,
        brightness_range=[-0.5, 0.5],
        rotation_range=[0.75, 1.25],
        shear_range=[0.75, 1.25],
        fill_mode='nearest'
    )
    val_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_dataframe(
        df_train,
        x_col = "filepath",
        y_col = "label",
        target_size=(img_size, img_size),
        batch_size=batch_size,
        class_mode='binary',
        validate_filenames=True
    )
    val_generator = val_datagen.flow_from_dataframe(
        df_val,
        x_col = "filepath",
        y_col = "label",
        target_size=(img_size, img_size),
        batch_size=batch_size,
        class_mode='binary',
        validate_filenames=True
    )

    return df_train, df_val, train_generator, val_generator

# MODEL PREPARATION #
def modelPrep(base_model: Model):
    pretrained_model = base_model(
        weights='imagenet',
        include_top=False,
        input_shape=(img_size, img_size, 3)
    )

    # CAN ADJUST STRUCTURE HERE #
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
    # pretrained_model.trainable = True
    # model.summary(show_trainable=True)

    model.compile(
        optimizer=Adam(learning_rate),
        loss=BinaryCrossentropy(from_logits=True),
        metrics=[BinaryAccuracy()]
    )
    return model

# MODEL TRAINING #
def modelTrain(model, train_gen, val_gen, epochs, callbacks: list = []):

    #latest = latest_checkpoint(os.path.join(os.path(os.getcwd(), checkpoint_dir)))
    #model.load_weights(latest)
    history = model.fit_generator(
        train_gen,
        epochs=epochs,
        steps_per_epoch=(train_gen.samples // train_gen.batch_size),
        validation_data=val_gen,
        validation_steps=(val_gen.samples // val_gen.batch_size),
        callback=callbacks,
        verbose=1
    )

    return history

def modelSave(model, name):
    model.save(f"{output_dir}/deepfake-{name}.keras")

def modelEvaluate(model, val_gen):
    val_loss, val_accuracy = model.evaluate(val_gen, verbose=2)
    # val_loss, val_accuracy = model.evaluate(x_val, y_val, verbose=2)
    # print(f'Validation Accuracy: {val_accuracy:.4f}')
    # print(f'Validation Loss: {val_loss:.4f}')

    # TODO(liam): make some plots; find F1 score maybe
    pass


if __name__ == '__main__':

    # df's are passed only to ensure they stay alive after function call
    df_train, df_val, train_datagen, test_datagen = dataLoad(dataset_name)

    # pass the function itself without initializing (fp)
    model = modelPrep(model_pretrained)

    latest = latest_checkpoint(os.path.join(os.getcwd(), checkpoint_dir))
    if (latest):
        model.load_weights(latest)

    callbacks = []
    callbacks.append(
        ModelCheckpoint(
            filepath=os.path.join(os.getcwd(), checkpoint_dir, checkpoint_path),
            save_weights_only=True,
            save_freq=5 * batch_size,
            verbose=1
        )
    )

    modelTrain(model, epochs, callbacks)

    modelEvaluate(model, test_datagen)

    modelSave(model, model_name)
