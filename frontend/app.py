from flask import Flask, request, render_template, url_for
import tensorflow as tf
import numpy as np
import os
from werkzeug.utils import secure_filename
from tensorflow.keras.preprocessing import image

app = Flask(__name__)

# Load the trained model
MODEL_PATH = r"C:\Users\Admin\Downloads\trafficdetection_model.keras"
model = tf.keras.models.load_model(MODEL_PATH)

# Folder to save uploaded images
UPLOAD_FOLDER = "C:\\Users\\Admin\\Downloads\\traffic dataset\\procode\\uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to preprocess image
def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return img_array

# Function to predict image
def predict_image(img_path):
    img_array = preprocess_image(img_path)
    predictions = model.predict(img_array)
    if predictions[0][0] > 0.3:
        return "🚦 Violation Detected"
    else:
        return "✅ No Violation Detected"

@app.route("/", methods=["GET", "POST"])
def upload_image():
    prediction = None
    image_url = None
    error = None

    if request.method == "POST":
        if "file" not in request.files:
            error = "No file part"
        else:
            file = request.files["file"]
            if file.filename == "":
                error = "No selected file"
            if file:
                try:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                    file.save(file_path)

                    # Get prediction
                    prediction = predict_image(file_path)
                    image_url = url_for('static', filename=f"uploads/{filename}")
                    print(f"Prediction: {filename} - {prediction}")
                except Exception as e:
                    error = f"An error occurred: {e}"

    return render_template("index.html", prediction=prediction, error=error, image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True)
