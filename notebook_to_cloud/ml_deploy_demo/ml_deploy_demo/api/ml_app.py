import logging

from flask import Blueprint, request, jsonify

from ml_deploy_demo.predict import predict_online
from ml_deploy_demo.util.utils import initialize_logging

logger = logging.getLogger(__name__)
initialize_logging(config_path='/app/logging.yaml')
ml_app = Blueprint("ml_app", __name__)

@ml_app.route("/predict", methods=["GET", "POST"])
def predict():
    """Performs an inference
    """
    if request.method == "POST":
        data = request.get_json()
        logger.debug(f"Input to predict/: {data}")
        pred = predict_online(data=data["data"])
        return jsonify({"input": data, "pred": pred})

    if request.method == "GET":
        msg = f"Please compose your request in POST type with data."
        logger.debug(f"Wrong request type {request}.")
        return jsonify({"msg": msg})
