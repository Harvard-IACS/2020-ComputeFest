import logging

import click

from util.utils import initialize_logging, load_yaml


logger = logging.getLogger(__name__)


# @note: https://click.palletsprojects.com/en/7.x/
@click.command()
@click.argument(
    "exp_config_path",
    default="/app/experiment_configs/default.yaml",
    type=click.Path(exists=True),
)
def predict(exp_config_path):
    """
    Simple
    """
    # read off a config file that controls experiment parameters.
    config = load_yaml(exp_config_path)

    log_config_path = config["logging"]["config_path"]
    initialize_logging(config_path=log_config_path)

    # load model

    # predict


if __name__ == "__main__":
    predict()
