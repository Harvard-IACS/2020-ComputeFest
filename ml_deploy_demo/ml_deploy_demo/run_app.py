import logging
from ml_app.app import initialize_app

logger = logging.getLogger(__name__)

app = initialize_app()

if __name__ == "__main__":
    logger.info("Initializing a Flask app...")
    app.run(debug=True)
