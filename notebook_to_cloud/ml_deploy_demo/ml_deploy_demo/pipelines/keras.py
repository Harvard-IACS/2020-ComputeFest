import os
import re
from pathlib import Path
import logging
import joblib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_datasets as tfds

from ml_deploy_demo.util.utils import load_yaml, initialize_logging

DEFAULT_CONFIG_PATH = "/app/experiment_configs/default.yaml"

logger = logging.getLogger(__name__)
config = load_yaml(DEFAULT_CONFIG_PATH)
config = config["train"]
log_config_path = config["logging"]["config_path"]
initialize_logging(config_path=log_config_path)

# This example is taken from:
# https://www.tensorflow.org/tutorials/keras/text_classification_with_hub

def run_pipeline():
    """ runs pipeline to train keras DNN model
        for sentiment classification """

    # Split the training set into 60% and 40%, so we'll end up with 15,000 examples
    # for training, 10,000 examples for validation and 25,000 examples for testing.
    train_validation_split = tfds.Split.TRAIN.subsplit([6, 4])

    (train_data, validation_data), test_data = tfds.load(
        name="imdb_reviews",
        split=(train_validation_split, tfds.Split.TEST),
        as_supervised=True)

    # Word Embeddings from Tensorflow-Hub
    embedding = "https://tfhub.dev/google/tf2-preview/gnews-swivel-20dim/1"
    hub_layer = hub.KerasLayer(embedding, input_shape=[],
                               dtype=tf.string, trainable=True)

    # Model
    model = tf.keras.Sequential()
    model.add(hub_layer)
    for _ in range(config['model']['params']['hidden_layers']):
        model.add(tf.keras.layers.Dense(
            config['model']['params']['hidden_units'],
            activation='relu'))
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

    # Compilation
    model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

    # Train
    history = model.fit(train_data.shuffle(10000).batch(512),
                    epochs=config['model']['params']['num_epochs'],
                    validation_data=validation_data.batch(512),
                    verbose=1)
    # Test
    results = model.evaluate(test_data.batch(512), verbose=2)

    for name, value in zip(model.metrics_names, results):
        logger.info("%s: %.3f" % (name, value))

    # Save
    model_name = config["model"]["name"]
    save_path = os.path.join(config["experiment"]["output_dirname"], f"{model_name}.keras")
    model.save(save_path)
    logger.info(f"Saved keras pipeline model at {save_path}")

    # Load & Check Consistency
    checkpoint = load_keras_hub_model(save_path)
    check_data = test_data.batch(512)
    assert np.all(
        checkpoint.predict(check_data) == model.predict(check_data)
    )
    logger.info("Keras saved model passed consistency check")

def load_keras_hub_model(save_path):
    return tf.keras.models.load_model(save_path,
        custom_objects={'KerasLayer': hub.KerasLayer}
    )

if __name__ == "__main__":
    run_pipeline()
