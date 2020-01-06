import logging

from flask import Blueprint, request, jsonify


logger =  logging.getLogger(__name__)

ml_app = Blueprint('ml_app', __name__)


@ml_app.route("/predict", methods=["GET", "POST"])
def predict():
    """
    """
    if request.method == "POST":
        data = request.get_json()
        logger.debug(f"Input to predict/: {data}")
        return jsonify({"output": "hello post" })

    if request.method == "GET":
        data = request.get_json()
        logger.debug(f"Input to predict/: {data}")
        return jsonify({"output": "hello get" })


