import logging

from flask import Blueprint, request, jsonify

from ml_deploy_demo.predict import predict_online
from ml_deploy_demo.style_transfer import style_transfer
# from ml_deploy_demo.util.utils import initialize_logging, load_yaml

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
ml_app = Blueprint("ml_app", __name__)


@ml_app.route("/predict", methods=["GET", "POST"])
def predict():
    """Performs an inference, or if 'is_style_transfer'==True
       is received, runs style transfer optimization
    """
    if request.method == "POST":
        data = request.get_json()
        logger.debug(f"Input to predict/: {data}")

        # if 'is_style_transfer' in data and data['is_style_transfer']:
            # request with "is_style_transfer" == True
            # => run style transfer, return "DONE" instead of
            # a prediction from a model. output saved to disk
        # logger.debug("Running style_transfer")
        params = {
        	'base_img_path' : 'data/cat_frame1.png',
        	'style_img_path' : 'data/starry_night_small.jpg',
        	'output_img_path' : 'experiment_output/style_transfer/cat_frame1_starrynight',
        	'convnet' : 'vgg16',
        	'content_weight' : 300,
        	'style_weights' : (10, 10, 50, 10, 10),
        	'tv_weight' : 300,
        	'content_layer' : 'block4_conv2',
        	'style_layers' : ['block1_conv1',
        					  'block2_conv1',
        					  'block3_conv1',
        					  'block4_conv1',
        					  'block5_conv1'],
        	'iterations' : 50,
        	'preserve_color' : False
        }
        print("running style transfer")
        style_transfer(**params)
        pred = "DONE"
        # else:
            # logger.debug("Running predict_online")
            # pred = predict_online(data=data["data"])

        return jsonify({"input": data, "pred": pred})

    if request.method == "GET":
        msg = f"Please compose your request in POST type with data."
        logger.debug(f"Wrong request type {request}.")
        return jsonify({"msg": msg})
