# Plant Disease Classification Model

This package contains a pre-trained EfficientNetB1 model for classifying plant diseases across 15 categories.

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

```python
from predict import PlantDiseaseClassifier

# Initialize classifier
classifier = PlantDiseaseClassifier(
    model_path='model/EfficientNetB1-plants-99.47.h5',
    class_mapping_path='model/plants-15.txt'
)

# Single image prediction
class_name, probability = classifier.predict('path/to/image.jpg')
print(f"Disease: {class_name} ({probability:.2f}%)")

# Batch prediction
results = classifier.predict_batch(['img1.jpg', 'img2.jpg'])
for result in results:
    print(f"{result['file']}: {result['class']} ({result['probability']:.2f}%)")
```

## Model Information

- Architecture: EfficientNetB1
- Input size: 224x224x3
- Number of classes: 15
- Training framework: TensorFlow/Keras

## Preprocessing Details

The model expects:
- RGB images
- Size: 224x224 pixels
- No normalization (EfficientNet handles this internally)
- Images are automatically resized if needed

## Classes

The model can classify the following plant diseases:

**Pepper:**
- Pepper__bell___Bacterial_spot
- Pepper__bell___healthy

**Potato:**
- Potato___Early_blight
- Potato___Late_blight
- Potato___healthy

**Tomato:**
- Tomato__Target_Spot
- Tomato__Tomato_YellowLeaf__Curl_Virus
- Tomato__Tomato_mosaic_virus
- Tomato_Bacterial_spot
- Tomato_Early_blight
- Tomato_Late_blight
- Tomato_Leaf_Mold
- Tomato_Septoria_leaf_spot
- Tomato_Spider_mites_Two_spotted_spider_mite
- Tomato_healthy

## API Reference

### PlantDiseaseClassifier

#### `__init__(model_path, class_mapping_path)`
Initialize the classifier with paths to the model and class mapping files.

#### `predict(image_path)`
Predict the disease class for a single image.

**Returns:** `(class_name, probability)`

#### `predict_batch(image_paths)`
Predict disease classes for multiple images.

**Returns:** List of dictionaries with keys: `file`, `class`, `probability`

## Troubleshooting

1. **ImportError:** Make sure all requirements are installed
2. **FileNotFoundError:** Check that image paths are correct
3. **Memory issues:** For large batches, process images in smaller chunks
4. **GPU support:** Install `tensorflow-gpu` for GPU acceleration

## License

This model is provided for educational and research purposes.
