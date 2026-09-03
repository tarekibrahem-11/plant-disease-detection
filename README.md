# 🌿 Plant Disease Detection

An AI-powered web application for detecting plant diseases from leaf images using Deep Learning and Generative AI.

The application uses a pretrained EfficientNetB1 model to classify plant leaf images into 15 different classes covering Pepper, Potato, and Tomato plants.

After detecting the disease, Google Gemini AI provides additional information about the detected condition, including symptoms, causes, treatment, and prevention.

---

## ✨ Features

- 🌱 Plant disease detection from leaf images
- 🧠 EfficientNetB1 deep learning model
- 🎯 15 plant disease and healthy classes
- 📊 Prediction confidence score
- 🤖 Google Gemini AI integration
- 🩺 AI-generated disease information
- 💊 Treatment and management recommendations
- 🛡️ Disease prevention information
- 📜 Prediction history
- 🔎 View previous prediction details
- 🗑️ Delete individual history records
- 🧹 Clear prediction history
- 🌐 Flask web application
- 🗄️ SQLite database
- 📸 Image upload validation

---

## 🖥️ Application Preview

The application provides a simple web interface where users can upload a plant leaf image and receive an AI-powered diagnosis.

### Home Page

![Plant Disease Detection](<img width="1919" height="918" alt="Screenshot 2026-09-02 191850" src="https://github.com/user-attachments/assets/8ff53ab7-b68e-4f3e-8760-1b5ce64a539f" />
)

---

## 🧠 AI Architecture

The application combines two AI components.

### 1. Deep Learning Classification

A pretrained EfficientNetB1 model analyzes the uploaded plant leaf image and predicts the most likely class.

**Model Specifications:**

- Architecture: EfficientNetB1
- Framework: TensorFlow / Keras
- Input Size: `224 × 224 × 3`
- Number of Classes: `15`
- Reported Accuracy: `99.47%`

---

## 🌿 Supported Classes

### 🌶️ Pepper

- `Pepper__bell___Bacterial_spot`
- `Pepper__bell___healthy`

### 🥔 Potato

- `Potato___Early_blight`
- `Potato___Late_blight`
- `Potato___healthy`

### 🍅 Tomato

- `Tomato__Target_Spot`
- `Tomato__Tomato_YellowLeaf__Curl_Virus`
- `Tomato__Tomato_mosaic_virus`
- `Tomato_Bacterial_spot`
- `Tomato_Early_blight`
- `Tomato_Late_blight`
- `Tomato_Leaf_Mold`
- `Tomato_Septoria_leaf_spot`
- `Tomato_Spider_mites_Two_spotted_spider_mite`
- `Tomato_healthy`

---

## 🔄 How It Works

```text
User uploads plant leaf image
            ↓
       Flask Web App
            ↓
    Image preprocessing
            ↓
    EfficientNetB1 Model
            ↓
     Disease prediction
            ↓
    Prediction confidence
            ↓
       Google Gemini
            ↓
Disease information & recommendations
            ↓
       SQLite History
