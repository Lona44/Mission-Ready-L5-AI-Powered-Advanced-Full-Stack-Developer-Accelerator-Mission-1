#!/usr/bin/env python3
"""
Local ONNX Model Testing Script
Tests car classification models before Azure deployment
"""

import json
import numpy as np
from PIL import Image
import onnxruntime as ort
from pathlib import Path

# ImageNet normalization values (models were trained with these)
IMAGENET_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
IMAGENET_STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)

def preprocess_image(image_path, image_size=224):
    """
    Preprocess image for model inference
    Same preprocessing as training
    """
    # Load and convert to RGB
    img = Image.open(image_path).convert('RGB')

    # Resize to model input size
    img = img.resize((image_size, image_size), Image.Resampling.BILINEAR)

    # Convert to numpy array and normalize to [0, 1]
    img_array = np.array(img, dtype=np.float32) / 255.0

    # Normalize with ImageNet mean/std
    img_array = (img_array - IMAGENET_MEAN) / IMAGENET_STD

    # Transpose to CHW format (channels first) and add batch dimension
    img_array = np.transpose(img_array, (2, 0, 1))  # HWC -> CHW
    img_array = np.expand_dims(img_array, axis=0)   # Add batch dimension

    return img_array

def load_model(model_path):
    """Load ONNX model"""
    print(f"Loading model: {model_path}")
    session = ort.InferenceSession(model_path)
    print(f"✅ Model loaded successfully")
    print(f"   Input name: {session.get_inputs()[0].name}")
    print(f"   Input shape: {session.get_inputs()[0].shape}")
    return session

def load_class_labels(labels_path):
    """Load class labels from JSON"""
    with open(labels_path, 'r') as f:
        labels = json.load(f)
    return labels

def predict(session, image_array, class_labels):
    """Run inference and return predictions"""
    # Get input name
    input_name = session.get_inputs()[0].name

    # Run inference
    outputs = session.run(None, {input_name: image_array})
    logits = outputs[0][0]  # Get first batch

    # Apply softmax to get probabilities
    exp_logits = np.exp(logits - np.max(logits))  # Subtract max for numerical stability
    probabilities = exp_logits / np.sum(exp_logits)

    # Get top 5 predictions
    top_indices = np.argsort(probabilities)[::-1][:5]

    results = []
    for idx in top_indices:
        # Handle different JSON formats
        if isinstance(class_labels, dict):
            if 'idx_to_class' in class_labels:
                class_name = class_labels['idx_to_class'][str(idx)]
            elif 'classes' in class_labels:
                class_name = class_labels['classes'][idx]
            else:
                class_name = f"Class {idx}"
        else:
            class_name = class_labels[idx]

        confidence = float(probabilities[idx])
        results.append({
            'class': class_name,
            'confidence': confidence,
            'confidence_pct': confidence * 100
        })

    return results

def test_body_type_model(image_path):
    """Test the body type classification model"""
    print("\n" + "="*60)
    print("TESTING BODY TYPE CLASSIFIER")
    print("="*60)

    model_path = "models/final/car_body_type_classifier.onnx"
    labels_path = "models/final/class_labels_body_type.json"

    # Load model and labels
    session = load_model(model_path)
    class_labels = load_class_labels(labels_path)

    # Preprocess image
    print(f"\nPreprocessing image: {image_path}")
    image_array = preprocess_image(image_path)
    print(f"✅ Image preprocessed: shape {image_array.shape}")

    # Run prediction
    print("\nRunning inference...")
    results = predict(session, image_array, class_labels)

    # Display results
    print("\n📊 TOP 5 PREDICTIONS:")
    print("-" * 50)
    for i, result in enumerate(results, 1):
        bar = "█" * int(result['confidence_pct'] / 2)
        print(f"{i}. {result['class']:<15} {result['confidence_pct']:>6.2f}% {bar}")

    print(f"\n🎯 PREDICTED CLASS: {results[0]['class']}")
    print(f"   Confidence: {results[0]['confidence_pct']:.2f}%")

    return results

def test_brand_model(image_path):
    """Test the brand classification model"""
    print("\n" + "="*60)
    print("TESTING BRAND CLASSIFIER")
    print("="*60)

    model_path = "models/final/car_brand_classifier.onnx"
    labels_path = "models/final/class_labels_brand.json"

    # Load model and labels
    session = load_model(model_path)
    class_labels = load_class_labels(labels_path)

    # Preprocess image
    print(f"\nPreprocessing image: {image_path}")
    image_array = preprocess_image(image_path)
    print(f"✅ Image preprocessed: shape {image_array.shape}")

    # Run prediction
    print("\nRunning inference...")
    results = predict(session, image_array, class_labels)

    # Display results
    print("\n📊 TOP 5 PREDICTIONS:")
    print("-" * 50)
    for i, result in enumerate(results, 1):
        bar = "█" * int(result['confidence_pct'] / 2)
        print(f"{i}. {result['class']:<20} {result['confidence_pct']:>6.2f}% {bar}")

    print(f"\n🎯 PREDICTED BRAND: {results[0]['class']}")
    print(f"   Confidence: {results[0]['confidence_pct']:.2f}%")

    return results

def main():
    """Main testing function"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python test_models_local.py <image_path> [model_type]")
        print("\nmodel_type options:")
        print("  both (default) - Test both models")
        print("  body           - Test body type model only")
        print("  brand          - Test brand model only")
        print("\nExample:")
        print("  python test_models_local.py data/raw/Cars_Body_Type/test/Sedan/image.jpg")
        sys.exit(1)

    image_path = sys.argv[1]
    model_type = sys.argv[2] if len(sys.argv) > 2 else 'both'

    # Verify image exists
    if not Path(image_path).exists():
        print(f"❌ Error: Image not found: {image_path}")
        sys.exit(1)

    print(f"\n🚗 CAR CLASSIFICATION MODEL TESTER")
    print(f"Image: {image_path}")
    print(f"Model: {model_type}")

    try:
        if model_type in ['both', 'body']:
            body_results = test_body_type_model(image_path)

        if model_type in ['both', 'brand']:
            brand_results = test_brand_model(image_path)

        print("\n" + "="*60)
        print("✅ TESTING COMPLETE!")
        print("="*60)

    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
