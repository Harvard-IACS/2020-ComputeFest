import logging
import joblib
from pathlib import Path

import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

from sklearn.decomposition import KernelPCA
from sklearn.datasets import load_iris
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm

logger = logging.getLogger(__name__)


def run_sklearn_pipeline(config):
    """Demo of a sklearn pipeline.

    read:
    - https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html
    - https://gist.github.com/amberjrivera/8c5c145516f5a2e894681e16a8095b5c
    """
    # load iris data
    data = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.25, random_state=999
    )

    # import model
    model_name = config["model"]["name"]
    model_params = config["model"]["params"]
    # @note: compare the two cases
    # if you want to run reproducible experiments at scale,
    # you'd better not hard-code parameters like below in the source code.
    try:
        if model_name == "random_forest":
            # case - A
            clf = RandomForestClassifier(max_depth=2, random_state=999)
        elif model_name == "support_vector_machine":
            # case - B
            kernel = model_params["svm_kernel"]
            gamma = model_params["svm_gamma"]
            C = model_params["svm_C"]
            clf = svm.SVC(kernel=kernel, gamma=gamma, C=C)
        else:
            raise ValueError(f"Unsupported model_name was given {model_name}.")
    except Exception as e:
        logger.error(f"{e}")

    # create a pipeline
    pipeline = Pipeline([("kernel_pca", KernelPCA()), ("model", clf)])

    # train
    pipeline.fit(X_train, y_train)

    # evaluate
    y_pred = pipeline.predict(X_test)

    report = classification_report(y_test, y_pred)
    logger.info(f"Accuracy report:\n{report}")

    cm = confusion_matrix(y_test, y_pred)
    logger.info(f"Confusion Matrix:\n{cm}")

    save_path = Path(config["experiment"]["output_dirname"]) / f"{model_name}.joblib"
    save_sklearn_model(pipeline, save_path)
    logger.info(f"Saved sklearn pipeline model at {save_path}")

    # check that the saved model behaves the same as before
    checkpoint = load_sklearn_model(save_path)
    assert np.all(checkpoint.predict(X_test) == pipeline.predict(X_test))


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
