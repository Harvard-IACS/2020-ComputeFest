import logging
from pathlib import Path
import os

import click

from ml_deploy_demo.pipelines.sklearn import load_sklearn_model
from ml_deploy_demo.pipelines.keras import load_keras_hub_model
from ml_deploy_demo.util.utils import initialize_logging, load_yaml


DEFAULT_CONFIG_PATH = "/app/experiment_configs/default.yaml"

logger = logging.getLogger(__name__)


# @note: https://click.palletsprojects.com/en/7.x/
@click.command()
@click.argument(
    "exp_config_path", default=DEFAULT_CONFIG_PATH, type=click.Path(exists=True),
)
def predict(exp_config_path):
    """Make predictions from data.
    data (np.array): n x d array.

    Returns:
        pred (list): n - dimensional predictions.
    """
    raise NotImplementedError

    # read off a config file that controls experiment parameters.
    config = load_yaml(exp_config_path)
    config = config["predict"]

    log_config_path = config["logging"]["config_path"]
    initialize_logging(config_path=log_config_path)

    # set data to evaluate on
    # @todo: not implemented yet.
    val_data = config["dataset_path"]
    pred = predict_online(val_data, config)
    return pred


def predict_online(data, config=None):
    """Predict from in-memory data on the fly.
    """
    if config is None:
        logger.debug(
            "Config path was not explicitly passed. Falling back to default config."
        )
        config = load_yaml(DEFAULT_CONFIG_PATH)
        config = config["predict"]

        log_config_path = config["logging"]["config_path"]
        initialize_logging(config_path=log_config_path)

        model_dirname = config["model"]["dirname"]
        model_version = config["model"]["version"]
        MODEL_EXT = "keras" # joblib
        # model_path = Path(model_dirname) / f"v{model_version}.{MODEL_EXT}"
        model_path = os.path.join(model_dirname, f"v{model_version}.{MODEL_EXT}")

    try:
        # @todo: fix the hard coding
        # checkpoint = load_sklearn_model(model_path)
        checkpoint = load_keras_hub_model(model_path)
        pred = checkpoint.predict(data)
        # can't jsonify np array
        pred = pred.tolist()
        logger.info({"input": data, "pred": pred})
    except Exception as e:
        logger.error(f"{e}")
        pred = []

    return pred


if __name__ == "__main__":
    predict()
