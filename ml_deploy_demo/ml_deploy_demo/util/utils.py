import joblib
import logging
import logging.config
from pathlib import Path
import yaml


def load_yaml(yaml_path):
    try:
        with open(yaml_path, "r") as f:
            config = yaml.safe_load(f)
    except Exception as e:
        logging.error(f"Failed to load a yaml file due to {e}")
    return config


def initialize_logging(config_path, exp_dirname=None):
    """Initialize logger from path.
    """
    try:
        config = load_yaml(config_path)
    except Exception as e:
        logging.basicConfig(level=logging.INFO)
        logging.info(f"{e}. Falling back to default logger.")
    else:
        # if successful
        if exp_dirname is None:
            # @todo: fix this hard-coding.
            exp_dirname = Path("/app/log")

        for handler_name in config["handlers"]:
            handler = config["handlers"][handler_name]
            if "filename" in handler:
                # must be a file handler
                handler["filename"] = exp_dirname / handler["filename"]
        logging.config.dictConfig(config)
    finally:
        logging.info(f"Logging initialized.")


def save_sklearn_model(model, save_path):
    try:
        joblib.dump(model, save_path)
    except Exception as e:
        logger.error(f"{e}")


def load_sklearn_model(load_path):
    try:
        model = joblib.load(load_path)
    except Exception as e:
        logger.error(f"{e}")
    return model

