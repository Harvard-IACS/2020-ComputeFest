import logging
import logging.config
from pathlib import Path
import yaml

import coloredlogs


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
