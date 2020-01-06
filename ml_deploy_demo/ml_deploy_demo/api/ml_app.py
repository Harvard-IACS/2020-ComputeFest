import logging

from flask import Blueprint, request, jsonify

from ml_deploy_demo.pipelines.sklearn import load_sklearn_model

logger = logging.getLogger(__name__)
ml_app = Blueprint("ml_app", __name__)


@ml_app.route("/predict", methods=["GET", "POST"])
def predict():
    """Performs an inference
    """
    if request.method == "POST":
        data = request.get_json()
        logger.debug(f"Input to predict/: {data}")

        # load data
        pred = {}
        try:
            # @todo: fix the hard coding.
            save_path = "/app/experiment_output/2020-01-06_02-54-10/support_vector_machine.joblib"
            checkpoint = load_sklearn_model(save_path)
            pred = checkpoint.predict(data["data"])
            # can't jsonify np array
            pred = pred.tolist()
        except Exception as e:
            logger.errors(f"{e}")

        return jsonify({"input": data, "pred": pred})

    if request.method == "GET":
        msg = f"Please compose your request in POST type with data."
        logger.debug(f"Wrong request type {request}.")
        return jsonify({"msg": msg})
