from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
import torch.nn as nn
import timm
import numpy as np
from PIL import Image
import io
import base64
import json
import os
from google.cloud import storage

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
body_type_model = None
body_type_labels = None
brand_model = None
brand_labels = None
device = torch.device("cpu")  # Cloud Run uses CPU


def download_model_from_gcs(bucket_name, source_blob_name, dest_file_name):
    """Download a file from GCS."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(dest_file_name)


def load_pytorch_model(checkpoint_path, num_classes):
    """Load a PyTorch model from checkpoint."""
    # Create model architecture
    model = timm.create_model('tf_efficientnetv2_m.in21k_ft_in1k', pretrained=False, num_classes=num_classes)

    # Load checkpoint
    checkpoint = torch.load(checkpoint_path, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(device)
    model.eval()

    return model


@app.on_event("startup")
async def load_models():
    """Load models on startup."""
    global body_type_model, body_type_labels, brand_model, brand_labels

    bucket_name = os.environ.get("GCS_BUCKET", "car-classification-ml-coastal-hue")

    # Download and load body type model
    print("Loading body type model...")
    download_model_from_gcs(bucket_name, "models/body-type/best_model_body_type.pth", "/tmp/body_type.pth")
    download_model_from_gcs(bucket_name, "models/body-type/class_labels_body_type.json", "/tmp/body_type_labels.json")

    with open("/tmp/body_type_labels.json", "r") as f:
        body_type_labels = json.load(f)["class_names"]

    body_type_model = load_pytorch_model("/tmp/body_type.pth", len(body_type_labels))

    # Download and load brand model
    print("Loading brand model...")
    download_model_from_gcs(bucket_name, "models/brand/best_model_brand.pth", "/tmp/brand.pth")
    download_model_from_gcs(bucket_name, "models/brand/class_labels_brand.json", "/tmp/brand_labels.json")

    with open("/tmp/brand_labels.json", "r") as f:
        brand_labels = json.load(f)["classes"]

    brand_model = load_pytorch_model("/tmp/brand.pth", len(brand_labels))

    print("Models loaded successfully!")


def preprocess_image(image_b64: str) -> torch.Tensor:
    """Preprocess image for inference."""
    # Decode base64
    image_bytes = base64.b64decode(image_b64)
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # Resize
    image = image.resize((224, 224), Image.BILINEAR)

    # Convert to array and normalize
    image_array = np.array(image, dtype=np.float32) / 255.0

    # ImageNet normalization
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    image_array = (image_array - mean) / std

    # Transpose to CHW format and convert to tensor
    image_array = np.transpose(image_array, (2, 0, 1))
    image_tensor = torch.from_numpy(image_array).unsqueeze(0).to(device)

    return image_tensor


class PredictionRequest(BaseModel):
    image: str  # base64 encoded image


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/predict/body-type")
async def predict_body_type(request: PredictionRequest):
    """Predict car body type."""
    try:
        # Preprocess
        input_tensor = preprocess_image(request.image)

        # Run inference
        with torch.no_grad():
            outputs = body_type_model(input_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)[0]

        # Get top 3
        top_probs, top_indices = torch.topk(probabilities, k=3)

        predictions = []
        for prob, idx in zip(top_probs, top_indices):
            predictions.append({
                "class": body_type_labels[idx.item()],
                "confidence": float(prob.item())
            })

        return {
            "predicted_class": predictions[0]["class"],
            "confidence": predictions[0]["confidence"],
            "top_3_predictions": predictions
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/brand")
async def predict_brand(request: PredictionRequest):
    """Predict car brand."""
    try:
        # Preprocess
        input_tensor = preprocess_image(request.image)

        # Run inference
        with torch.no_grad():
            outputs = brand_model(input_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)[0]

        # Get top 5
        top_probs, top_indices = torch.topk(probabilities, k=5)

        predictions = []
        for prob, idx in zip(top_probs, top_indices):
            predictions.append({
                "class": brand_labels[idx.item()],
                "confidence": float(prob.item())
            })

        return {
            "predicted_class": predictions[0]["class"],
            "confidence": predictions[0]["confidence"],
            "top_5_predictions": predictions
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
