import logging
import logging.config
from pathlib import Path
import yaml

import coloredlogs

import numpy as np
from keras import backend as K
from keras.applications import vgg16
from keras.preprocessing.image import load_img, img_to_array

def load_yaml(yaml_path):
    try:
        with open(yaml_path, "r") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        logging.error(f"Failed to load a yaml file due to {e}")
    return config


def initialize_logging(config_path, log_dirname=None):
    """Initialize logger from path.
    """
    try:
        config = load_yaml(config_path)
    except Exception as e:
        # if fail
        logging.basicConfig(level=logging.INFO)
        logging.info(f"{e}. Falling back to default logger.")
    else:
        # if successful
        if log_dirname is not None:
            for handler_name in config["handlers"]:
                handler = config["handlers"][handler_name]
                if "filename" in handler:
                    # must be a file handler
                    filename = Path(handler["filename"]).name
                    handler["filename"] = log_dirname / filename

        # install coloredlogs for console handler only
        console_format = config["formatters"][
            config["handlers"]["console"]["formatter"]
        ]["format"]
        console_level = config["handlers"]["console"]["level"]
        console_stream = config["handlers"]["console"]["stream"]
        coloredlogs.install(fmt=console_format, level=console_level, sys=console_stream)

        logging.config.dictConfig(config)
    finally:
        logging.info(f"Logging initialized.")

def time_function(f, *args):
	"""
	Call a function f with args and return the time
	(in seconds) that it took to execute.
	"""
	tic = time.time()
	f(*args)
	toc = time.time()
	return toc - tic

# util function to open, resize and format pictures into appropriate tensors
def preprocess_image(image_path, desired_dims):
	img = load_img(image_path, target_size=desired_dims)
	img = img_to_array(img)
	img = np.expand_dims(img, axis=0)
	img = vgg16.preprocess_input(img)
	return img

# util function to convert a tensor into a valid image
def deprocess_image(x, img_nrows, img_ncols):
	x = x.reshape((img_nrows, img_ncols, 3))
	# Remove zero-center by mean pixel
	x[:, :, 0] += 103.939
	x[:, :, 1] += 116.779
	x[:, :, 2] += 123.68
	# 'BGR'->'RGB'
	x = x[:, :, ::-1]
	x = np.clip(x, 0, 255).astype('uint8')
	return x
