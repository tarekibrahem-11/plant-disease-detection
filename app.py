import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import regularizers
import cv2
import warnings
from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    send_from_directory,
    jsonify,
)
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime
import sqlite3


warnings.filterwarnings("ignore")

# Flask app configuration
app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key-here"
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "webp"}

# Create upload folder if it doesn't exist
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


# Initialize database
def init_db():
    conn = sqlite3.connect("plant_disease.db")
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_name TEXT NOT NULL,
            probability REAL NOT NULL,
            image_path TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            ai_info TEXT
        )
    """
    )
    conn.commit()
    conn.close()


# Model constants
IMG_SIZE = (224, 224)
MODEL_PATH = "model/EfficientNetB1-plants-99.47.h5"
CLASS_MAPPING_PATH = "model/plants-15.txt"




def custom_depthwise_conv2d(*args, **kwargs):
    """Custom DepthwiseConv2D that removes 'groups' parameter"""
    if "groups" in kwargs:
        kwargs.pop("groups")
    return tf.keras.layers.DepthwiseConv2D(*args, **kwargs)


def load_model_with_compatibility(model_path):
    """Load model with version compatibility fixes"""
    try:
        model = tf.keras.models.load_model(model_path)
        print("✓ Model loaded successfully (standard method)")
        return model
    except:
        try:
            custom_objects = {
                "l2": regularizers.l2,
                "l1": regularizers.l1,
                "L2": regularizers.L2,
                "L1": regularizers.L1,
            }
            model = tf.keras.models.load_model(
                model_path, custom_objects=custom_objects
            )
            print("✓ Model loaded successfully (with custom objects)")
            return model
        except:
            try:
                custom_objects = {
                    "DepthwiseConv2D": custom_depthwise_conv2d,
                    "l2": regularizers.l2,
                    "l1": regularizers.l1,
                    "L2": regularizers.L2,
                    "L1": regularizers.L1,
                }
                model = tf.keras.models.load_model(
                    model_path, custom_objects=custom_objects
                )
                print("✓ Model loaded successfully (with compatibility fixes)")
                return model
            except Exception as e:
                print(f"Error loading model: {e}")
                return None


def preprocess_image(image_path):
    """Preprocess image for prediction"""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not read image from {image_path}")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, IMG_SIZE)
    img = np.expand_dims(img, axis=0)

    return img


def load_class_mappings(dict_path):
    """Load class mappings from text file"""
    try:
        with open(dict_path, "r") as f:
            dict_text = f.read()
            class_dict = eval(dict_text)
        return class_dict
    except Exception as e:
        print(f"Error loading class mappings: {e}")
        default_classes = [
            "Pepper__bell___Bacterial_spot",
            "Pepper__bell___healthy",
            "Potato___Early_blight",
            "Potato___Late_blight",
            "Potato___healthy",
            "Tomato__Target_Spot",
            "Tomato__Tomato_YellowLeaf__Curl_Virus",
            "Tomato__Tomato_mosaic_virus",
            "Tomato_Bacterial_spot",
            "Tomato_Early_blight",
            "Tomato_Late_blight",
            "Tomato_Leaf_Mold",
            "Tomato_Septoria_leaf_spot",
            "Tomato_Spider_mites_Two_spotted_spider_mite",
            "Tomato_healthy",
        ]
        return {i: cls for i, cls in enumerate(default_classes)}



class PlantDiseaseClassifier:
    def __init__(self, model_path, class_mapping_path):
        self.model = load_model_with_compatibility(model_path)
        if self.model is None:
            raise ValueError("Failed to load model")

        self.class_mapping = load_class_mappings(class_mapping_path)
        self.classes = list(self.class_mapping.values())

        print(f"Model loaded with {len(self.classes)} classes")

    def predict(self, image_path):
        """Predict plant disease from image"""
        try:
            img = preprocess_image(image_path)
            pred = self.model.predict(img, verbose=0)

            index = np.argmax(pred[0])
            class_name = self.classes[index]
            probability = pred[0][index] * 100

            return class_name, probability

        except Exception as e:
            print(f"Prediction error: {e}")
            return None, 0.0


# Initialize the classifier globally
print("Loading model...")
classifier = PlantDiseaseClassifier(MODEL_PATH, CLASS_MAPPING_PATH)
print("Model loaded successfully!")


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/history")
def history():
    conn = sqlite3.connect("plant_disease.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM history ORDER BY timestamp DESC")
    history_items = c.fetchall()
    conn.close()
    return render_template("history.html", history=history_items)


@app.route("/history/<int:item_id>")
def history_detail(item_id):
    conn = sqlite3.connect("plant_disease.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM history WHERE id = ?", (item_id,))
    item = c.fetchone()
    conn.close()

    if item is None:
        flash("History item not found")
        return redirect(url_for("history"))

    result = {
        "id": item["id"],
        "class_name": item["class_name"],
        "probability": item["probability"],
        "image_path": item["image_path"],
        "timestamp": item["timestamp"],
        "ai_info": item["ai_info"] if item["ai_info"] else None,
    }

    return render_template("result.html", result=result, from_history=True)


    return jsonify({"info": info})
@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        flash("No file part")
        return redirect(url_for("index"))

    file = request.files["file"]

    if file.filename == "":
        flash("No selected file")
        return redirect(url_for("index"))

    if file and allowed_file(file.filename):
        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)

        # Save file
        file.save(filepath)

        # Make prediction
        try:
            class_name, probability = classifier.predict(filepath)

            if class_name:
                # Format the class name for display
                display_name = class_name.replace("_", " ").replace("  ", " - ")

                ai_info = None
                

                # Save to database
                conn = sqlite3.connect("plant_disease.db")
                c = conn.cursor()
                c.execute(
                    """
                    INSERT INTO history (class_name, probability, image_path, timestamp, ai_info)
                    VALUES (?, ?, ?, ?, ?)
                """,
                    (
                        display_name,
                        round(probability, 2),
                        unique_filename,
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        ai_info,
                    ),
                )
                result_id = c.lastrowid
                conn.commit()
                conn.close()

                result = {
                    "id": result_id,
                    "class_name": display_name,
                    "probability": round(probability, 2),
                    "image_path": unique_filename,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "ai_info": ai_info,
                }

                return render_template("result.html", result=result)
            else:
                flash("Error processing image")
                return redirect(url_for("index"))

        except Exception as e:
            flash(f"Error: {str(e)}")
            return redirect(url_for("index"))

    flash("Invalid file type. Please upload PNG, JPG, or JPEG files only.")
    return redirect(url_for("index"))


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/clear_history", methods=["POST"])
def clear_history():
    conn = sqlite3.connect("plant_disease.db")
    c = conn.cursor()
    c.execute("DELETE FROM history")
    conn.commit()
    conn.close()
    flash("History cleared successfully")
    return redirect(url_for("history"))


@app.route("/delete_history_item/<int:item_id>", methods=["POST"])
def delete_history_item(item_id):
    conn = sqlite3.connect("plant_disease.db")
    c = conn.cursor()

    # Get the image path before deleting the record
    c.execute("SELECT image_path FROM history WHERE id = ?", (item_id,))
    result = c.fetchone()

    if result:
        c.execute("DELETE FROM history WHERE id = ?", (item_id,))
        conn.commit()

        # Optionally delete the image file if not used by other records
        image_path = result[0]
        c.execute("SELECT COUNT(*) FROM history WHERE image_path = ?", (image_path,))
        count = c.fetchone()[0]

        if count == 0:
            try:
                full_path = os.path.join(app.config["UPLOAD_FOLDER"], image_path)
                if os.path.exists(full_path):
                    os.remove(full_path)
            except Exception as e:
                print(f"Error deleting file: {e}")

    conn.close()
    flash("History item deleted successfully")
    return redirect(url_for("history"))


@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500


# Initialize the database when the app starts
init_db()

if __name__ == "__main__":

    app.run(debug=False)
