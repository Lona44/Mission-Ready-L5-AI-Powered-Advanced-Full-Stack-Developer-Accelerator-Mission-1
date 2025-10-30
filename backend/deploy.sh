#!/bin/bash

# Deploy to Cloud Run
set -e

PROJECT_ID=$(~/google-cloud-sdk/bin/gcloud config get-value project)
REGION="us-central1"
SERVICE_NAME="car-classifier"

echo "======================================"
echo "Deploying to Cloud Run"
echo "======================================"
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo "Service: $SERVICE_NAME"
echo ""

# Step 1: Enable required APIs
echo "[1/3] Enabling required APIs..."
~/google-cloud-sdk/bin/gcloud services enable run.googleapis.com
~/google-cloud-sdk/bin/gcloud services enable cloudbuild.googleapis.com

# Step 2: Deploy to Cloud Run (builds automatically in cloud)
echo "[2/3] Deploying to Cloud Run..."
echo "This will build the container in the cloud and deploy it."
echo ""
echo "Note: Run this script from the backend/ directory"
echo ""

~/google-cloud-sdk/bin/gcloud run deploy ${SERVICE_NAME} \
  --source . \
  --region=${REGION} \
  --platform=managed \
  --allow-unauthenticated \
  --memory=4Gi \
  --cpu=2 \
  --timeout=600 \
  --max-instances=3 \
  --cpu-boost \
  --set-env-vars=GCS_BUCKET=car-classification-ml-coastal-hue

# Step 3: Get the service URL
echo ""
echo "[3/3] Getting service URL..."
SERVICE_URL=$(~/google-cloud-sdk/bin/gcloud run services describe ${SERVICE_NAME} --region=${REGION} --format='value(status.url)')

echo ""
echo "======================================"
echo "Deployment Complete!"
echo "======================================"
echo ""
echo "Service URL: ${SERVICE_URL}"
echo ""
echo "Test endpoints:"
echo ""
echo "Health check:"
echo "  curl ${SERVICE_URL}/health"
echo ""
echo "Body type prediction:"
echo "  curl -X POST ${SERVICE_URL}/predict/body-type \\"
echo "    -H \"Content-Type: application/json\" \\"
echo "    -d '{\"image\": \"BASE64_ENCODED_IMAGE\"}'"
echo ""
echo "Brand prediction:"
echo "  curl -X POST ${SERVICE_URL}/predict/brand \\"
echo "    -H \"Content-Type: application/json\" \\"
echo "    -d '{\"image\": \"BASE64_ENCODED_IMAGE\"}'"
echo ""
echo "Costs: Cloud Run charges only when handling requests"
echo "  - First 2 million requests/month: FREE"
echo "  - After that: ~\$0.40 per million requests"
echo "  - No cost when idle"
echo ""
