# Backend - ML API (GCP Cloud Run)

FastAPI-based machine learning API deployed on Google Cloud Run for car classification.

## Live Deployment

**Service URL**: `https://car-classifier-tilhbeahgq-uc.a.run.app`

**Status**: ✅ Operational

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/predict/body-type` | POST | Classify car body type (7 classes) |
| `/predict/brand` | POST | Classify car brand (33 classes) |

## Architecture

```
┌─────────────────────────────────────────┐
│     Google Cloud Run (Serverless)       │
│                                         │
│  FastAPI + PyTorch + EfficientNetV2-M  │
│  • 4GB RAM, 2 CPUs                     │
│  • Auto-scaling: 0-3 instances         │
│  • Cold start: ~30-60 seconds          │
│  • Warm response: ~1-3 seconds         │
│                                         │
│  Models loaded from Google Cloud        │
│  Storage (GCS) on startup               │
└─────────────────────────────────────────┘
```

## Files

| File | Purpose |
|------|---------|
| `main.py` | FastAPI application with model inference |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Container definition |
| `deploy.sh` | Deployment script for GCP Cloud Run |

## Local Development

### Prerequisites

- Python 3.11+
- Model files downloaded from Kaggle training (see `kaggle/`)
- Google Cloud SDK (for deployment only)

### Setup

1. **Install dependencies**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Download models** (if not already done)
   - Place `.pth` model files in `models/checkpoints/`
   - Place `class_labels_*.json` in `models/final/`
   - Or download from GCS (if you have access):
     ```bash
     gsutil cp gs://car-classification-ml-coastal-hue/models/body-type/* models/checkpoints/
     gsutil cp gs://car-classification-ml-coastal-hue/models/brand/* models/checkpoints/
     ```

3. **Run locally** (requires models in GCS or modify code for local paths)
   ```bash
   python main.py
   ```
   Server runs on `http://localhost:8080`

## Testing the API

### Health Check

```bash
curl https://car-classifier-tilhbeahgq-uc.a.run.app/health
```

Expected: `{"status":"healthy"}`

### Predict Body Type

```bash
# Encode image to base64
IMAGE_B64=$(base64 -i path/to/car.jpg)

# Make prediction
curl -X POST https://car-classifier-tilhbeahgq-uc.a.run.app/predict/body-type \
  -H "Content-Type: application/json" \
  -d "{\"image\": \"$IMAGE_B64\"}"
```

Response:
```json
{
  "predicted_class": "Pick-Up",
  "confidence": 1.0,
  "top_3_predictions": [
    {"class": "Pick-Up", "confidence": 1.0},
    {"class": "Sedan", "confidence": 0.00000003},
    {"class": "SUV", "confidence": 0.00000001}
  ]
}
```

### Predict Brand

```bash
curl -X POST https://car-classifier-tilhbeahgq-uc.a.run.app/predict/brand \
  -H "Content-Type: application/json" \
  -d "{\"image\": \"$IMAGE_B64\"}"
```

Response:
```json
{
  "predicted_class": "Ram",
  "confidence": 0.981,
  "top_5_predictions": [
    {"class": "Ram", "confidence": 0.981},
    {"class": "Dodge", "confidence": 0.009},
    {"class": "Ford", "confidence": 0.009},
    {"class": "Lincoln", "confidence": 0.001},
    {"class": "BMW", "confidence": 0.00003}
  ]
}
```

## Deployment

### Prerequisites

1. **Google Cloud SDK installed**
   ```bash
   # macOS
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL

   # Initialize
   gcloud init
   ```

2. **GCP Project setup**
   - Project ID: `coastal-hue-476619-u5` (or your project)
   - Billing enabled
   - Cloud Run API enabled
   - Cloud Build API enabled

3. **Models uploaded to GCS**
   ```bash
   gsutil cp models/checkpoints/best_model_body_type.pth \
     gs://car-classification-ml-coastal-hue/models/body-type/

   gsutil cp models/checkpoints/best_model_brand.pth \
     gs://car-classification-ml-coastal-hue/models/brand/

   gsutil cp models/final/class_labels_*.json \
     gs://car-classification-ml-coastal-hue/models/*/
   ```

### Deploy to Cloud Run

```bash
cd backend
./deploy.sh
```

This script will:
1. Enable required GCP APIs
2. Build Docker container in the cloud
3. Deploy to Cloud Run with optimal configuration
4. Make the service publicly accessible
5. Output the service URL

**Deployment takes ~5-10 minutes**

### Manual Deployment

If the script doesn't work, deploy manually:

```bash
gcloud run deploy car-classifier \
  --source . \
  --region=us-central1 \
  --platform=managed \
  --allow-unauthenticated \
  --memory=4Gi \
  --cpu=2 \
  --timeout=600 \
  --max-instances=3 \
  --cpu-boost \
  --set-env-vars=GCS_BUCKET=car-classification-ml-coastal-hue
```

## Cost Management

### Pricing (as of 2024)

**Cloud Run (Pay-per-use)**
- First 2 million requests/month: **FREE**
- After that: ~$0.40 per million requests
- Memory: $0.000024 per GB-second
- CPU: $0.000024 per vCPU-second
- No cost when idle

**Our configuration cost**:
- ~$0.29 per 1,000 requests
- Typical usage: <10,000 requests/month = **FREE**

### Cost Optimization

1. **Auto-scaling to zero**
   - Service automatically scales down when not in use
   - No cost when idle (unlike always-on servers)

2. **Set up billing alerts** (recommended)
   - See `docs/SETUP_BILLING_ALERTS.md`
   - Get notified at $25, $45, $50 spending

3. **Monitor usage**
   ```bash
   gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=car-classifier" --limit=50
   ```

4. **Delete service when not needed**
   ```bash
   gcloud run services delete car-classifier --region=us-central1
   ```

## Technical Decisions

### Why Cloud Run (not Vertex AI)?

| Cloud Run | Vertex AI |
|-----------|-----------|
| ✅ Pay-per-request | ❌ Pay 24/7 for VM |
| ✅ Auto-scales to zero | ❌ Minimum 1 replica |
| ✅ $0-5/month typical | ❌ $70-200/month |
| ✅ Perfect for demos | ✅ Better for production scale |
| ❌ Cold start delays | ✅ Always warm |

**Verdict**: Cloud Run is ideal for student projects and portfolios.

### Why PyTorch (not ONNX)?

Cloud Run's security policies prevent ONNX Runtime from working (executable stack requirement). PyTorch runs without issues and provides identical predictions.

## Troubleshooting

### Cold Start Taking Too Long

**Symptom**: First request takes 30-60 seconds
**Cause**: Cloud Run downloads 1.2GB of models from GCS on startup
**Solution**: This is normal. Subsequent requests are fast (1-3 seconds)

**Optional fix** (costs money):
```bash
# Keep 1 instance always warm (costs ~$30/month)
gcloud run services update car-classifier \
  --region=us-central1 \
  --min-instances=1
```

### Out of Memory Error

**Symptom**: Container crashes or 500 errors
**Solution**: Increase memory allocation
```bash
gcloud run services update car-classifier \
  --region=us-central1 \
  --memory=8Gi
```

### 403 Forbidden

**Symptom**: Cannot access endpoints
**Cause**: Service is not public
**Solution**:
```bash
gcloud run services add-iam-policy-binding car-classifier \
  --region=us-central1 \
  --member=allUsers \
  --role=roles/run.invoker
```

## Further Documentation

- Full deployment guide: `docs/GCP_DEPLOYMENT_GUIDE.md`
- Deployment log with hurdles: `docs/DEPLOYMENT_LOG.md`
- Billing setup: `docs/SETUP_BILLING_ALERTS.md`

## Security Note

The API is **publicly accessible** (no authentication). This is intentional for easy frontend integration and demos. For production use, implement:
- API key authentication
- Rate limiting
- CORS restrictions
- Request validation
