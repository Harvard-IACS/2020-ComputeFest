import logging
from pathlib import Path
from datetime import datetime

import click

from ml_deploy_demo.pipelines.sklearn import run_sklearn_pipeline
from ml_deploy_demo.util.utils import initialize_logging, load_yaml


logger = logging.getLogger(__name__)


# @note: https://click.palletsprojects.com/en/7.x/
@click.command()
@click.argument(
    "exp_config_path",
    default="/app/experiment_configs/default.yaml",
    type=click.Path(exists=True),
)
def main(exp_config_path):
    """
    Simple
    """
    # read off a config file that controls experiment parameters.
    config = load_yaml(exp_config_path)
    config = config["train"]

    # determine an output path where results of an experiment are stored.
    cur_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    exp_output_dirname = Path(config["experiment"]["output_dirname"]) / cur_time
    config["experiment"]["output_dirname"] = exp_output_dirname

    if not exp_output_dirname.exists():
        Path.mkdir(exp_output_dirname, exist_ok=True)

    # initialize loggers
    # @note: log files are stored to each exp_dirname.
    #        this is more useful for machine learning pipelines.
    #        as opposed to a standard web app where it has centralized log.
    #        for other modules other than train.py we log to the centralized.
    log_config_path = config["logging"]["config_path"]
    initialize_logging(config_path=log_config_path, log_dirname=exp_output_dirname)

    # a demo of a training pipeline using sklearn Pipeline
    # @todo: add more pipelines: e.g. tensorflow, pytorch
    if config["data"]["dataset_name"] == "iris":
        run_sklearn_pipeline(config)
    else:
        raise ValueError(f"Unsupported dataset was given {config['data']}.")


if __name__ == "__main__":
    main()
