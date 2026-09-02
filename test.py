import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import regularizers
import cv2
import warnings
import json
warnings.filterwarnings('ignore')

# Model constants
IMG_SIZE = (224, 224)

def custom_depthwise_conv2d(*args, **kwargs):
    """Custom DepthwiseConv2D that removes 'groups' parameter"""
    if 'groups' in kwargs:
        kwargs.pop('groups')
    return tf.keras.layers.DepthwiseConv2D(*args, **kwargs)

def load_model_with_compatibility(model_path):
    """Load model with version compatibility fixes"""
    try:
        # First attempt: standard loading
        model = tf.keras.models.load_model(model_path)
        print("✓ Model loaded successfully (standard method)")
        return model
    except:
        try:
            # Second attempt: with custom objects for regularizers
            custom_objects = {
                'l2': regularizers.l2,
                'l1': regularizers.l1,
                'L2': regularizers.L2,
                'L1': regularizers.L1
            }
            model = tf.keras.models.load_model(model_path, custom_objects=custom_objects)
            print("✓ Model loaded successfully (with custom objects)")
            return model
        except:
            try:
                # Third attempt: handle DepthwiseConv2D compatibility
                custom_objects = {
                    'DepthwiseConv2D': custom_depthwise_conv2d,
                    'l2': regularizers.l2,
                    'l1': regularizers.l1,
                    'L2': regularizers.L2,
                    'L1': regularizers.L1
                }
                model = tf.keras.models.load_model(model_path, custom_objects=custom_objects)
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
    
    # Convert BGR to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Resize to model input size
    img = cv2.resize(img, IMG_SIZE)
    
    # No normalization needed for EfficientNet
    img = np.expand_dims(img, axis=0)
    
    return img

def load_class_mappings(dict_path):
    """Load class mappings from text file"""
    try:
        with open(dict_path, 'r') as f:
            dict_text = f.read()
            class_dict = eval(dict_text)
        return class_dict
    except Exception as e:
        print(f"Error loading class mappings: {e}")
        # Fallback: create default mapping
        default_classes = [
            'Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy',
            'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
            'Tomato__Target_Spot', 'Tomato__Tomato_YellowLeaf__Curl_Virus',
            'Tomato__Tomato_mosaic_virus', 'Tomato_Bacterial_spot',
            'Tomato_Early_blight', 'Tomato_Late_blight', 'Tomato_Leaf_Mold',
            'Tomato_Septoria_leaf_spot', 'Tomato_Spider_mites_Two_spotted_spider_mite',
            'Tomato_healthy'
        ]
        return {i: cls for i, cls in enumerate(default_classes)}

class PlantDiseaseClassifier:
    def __init__(self, model_path, class_mapping_path):
        # Load model with compatibility fixes
        self.model = load_model_with_compatibility(model_path)
        if self.model is None:
            raise ValueError("Failed to load model")
        
        # Load class mappings
        self.class_mapping = load_class_mappings(class_mapping_path)
        self.classes = list(self.class_mapping.values())
        
        print(f"Model loaded with {len(self.classes)} classes")
    
    def predict(self, image_path):
        """Predict plant disease from image"""
        try:
            # Preprocess image
            img = preprocess_image(image_path)
            
            # Make prediction
            pred = self.model.predict(img, verbose=0)
            
            # Get predicted class
            index = np.argmax(pred[0])
            class_name = self.classes[index]
            probability = pred[0][index] * 100
            
            return class_name, probability
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return None, 0.0

# Example usage
if __name__ == "__main__":
    # Initialize classifier
    classifier = PlantDiseaseClassifier(
        model_path='model/EfficientNetB1-plants-99.47.h5',
        class_mapping_path='model/plants-15.txt'
    )
    
    # Test on the specific image
    image_path = r'C:\Users\amrda\Downloads\plant_disease_model\plant_disease_model\plant_disease_samples\Tomato__Tomato_YellowLeaf__Curl_Virus\7c8981a1-fcac-441b-9f68-03e275441eb6___UF.GRC_YLCV_Lab 02853.JPG'
    
    if os.path.exists(image_path):
        class_name, probability = classifier.predict(image_path)
        if class_name:
            print(f"\nPrediction: {class_name} ({probability:.2f}%)")
        else:
            print("Prediction failed")
    else:
        print(f"Image not found: {image_path}")