# from flask import Flask
# from app.config.config import get_config_by_name
# from app.initialize_functions import initialize_route, initialize_db, initialize_swagger

# def create_app(config=None) -> Flask:
#     """
#     Create a Flask application.

#     Args:
#         config: The configuration object to use.

#     Returns:
#         A Flask application instance.
#     """
#     app = Flask(__name__)
#     if config:
#         app.config.from_object(get_config_by_name(config))

#     # Initialize extensions
#     initialize_db(app)

#     # Register blueprints
#     initialize_route(app)

#     # Initialize Swagger
#     initialize_swagger(app)

#     return app

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Disable TensorFlow INFO and WARNING messages

from flask import Flask, render_template, request, jsonify
import numpy as np
from tensorflow import keras
import cv2
import base64

# Initialize flask app
app = Flask(__name__)

# Load prebuilt model
model = keras.models.load_model('app/models/mnist_classification.h5')

# Handle GET request
@app.route('/', methods=['GET'])
def drawing():
    return render_template('drawing.html')

# Handle POST request
@app.route('/', methods=['POST'])
def canvas():
    # Recieve base64 data from the user form
    canvasdata = request.form['canvasimg']
    encoded_data = request.form['canvasimg'].split(',')[1]

    # Decode base64 image to python array
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Convert 3 channel image (RGB) to 1 channel image (GRAY)
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Resize to (28, 28)
    gray_image = cv2.resize(gray_image, (28, 28), interpolation=cv2.INTER_LINEAR)

    # Expand to numpy array dimension to (1, 28, 28)
    img = np.expand_dims(gray_image, axis=0)

    try:
        prediction = np.argmax(model.predict(img))
        print(f"Prediction Result : {str(prediction)}")
        return render_template('drawing.html', response=str(prediction), canvasdata=canvasdata, success=True)
    except Exception as e:
        return render_template('drawing.html', response=str(e), canvasdata=canvasdata)
