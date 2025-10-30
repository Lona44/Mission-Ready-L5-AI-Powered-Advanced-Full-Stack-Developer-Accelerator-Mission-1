# Vehicle Classification System - Turners Insurance

End-to-end ML system for automated vehicle classification from images, built for Turners Car Auctions' insurance division.

## Overview

AI-powered dual-model classification system that identifies vehicle body types and brands from photos to streamline insurance quote processing for Turners Insurance customers.

## System Architecture

**Training Platform**: Kaggle (free GPU)
**Backend API**: Google Cloud Platform (Cloud Run)
**Frontend**: Azure Static Web Apps
**Model Format**: PyTorch (.pth) + ONNX

### Hybrid Cloud Deployment
- **Backend**: GCP Cloud Run (serverless FastAPI)
- **Frontend**: Azure Static Web Apps (React + TailwindCSS)

## Model Performance

### Body Type Classification
- **Classes**: 7 (Sedan, SUV, Pick-Up, Convertible, Coupe, Hatchback, VAN)
- **Accuracy**: 97.6% on test set
- **Architecture**: EfficientNetV2-Medium (ImageNet-21k pretrained)
- **Dataset**: 7,549 images

### Brand Classification
- **Classes**: 33 brands (Ram, Ford, BMW, Toyota, etc.)
- **Accuracy**: 75.2% on test set
- **Architecture**: EfficientNetV2-Medium (ImageNet-21k pretrained)
- **Dataset**: 16,467 images

## Technology Stack

### Training
- **Platform**: Kaggle Notebooks (Tesla P100 GPU)
- **Framework**: PyTorch 2.x + TIMM
- **Model**: `tf_efficientnetv2_m.in21k_ft_in1k`
- **Training Time**: ~2.5 hours per model

### Backend API
- **Framework**: FastAPI
- **Runtime**: PyTorch (ONNX not compatible with Cloud Run)
- **Deployment**: GCP Cloud Run (serverless)
- **Features**: CORS-enabled, auto-scaling 0-3 instances

### Frontend
- **Framework**: React 18 + Vite
- **Styling**: TailwindCSS
- **API Client**: Axios
- **Deployment**: Azure Static Web Apps

## Project Structure

```
Mission_01/
├── kaggle/                  # Training notebooks and configs
│   ├── notebooks/           # Jupyter notebooks for Kaggle
│   └── config/             # Training hyperparameters
├── backend/                # GCP Cloud Run API
│   ├── main.py            # FastAPI application
│   ├── Dockerfile         # Container definition
│   └── deploy.sh          # Deployment script
├── frontend/              # React web application
│   ├── src/               # React components
│   └── dist/              # Production build
├── models/
│   ├── final/             # Class label mappings (JSON)
│   └── metrics/           # Training visualizations
└── data/                  # Datasets (gitignored)
```

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Kaggle account
- Google Cloud account
- Azure account

### Run Frontend Locally

```bash
cd frontend
npm install
npm run dev
```

Visit http://localhost:5173

### Deploy Backend to GCP

```bash
cd backend
./deploy.sh
```

Requires Google Cloud SDK and authentication.

## Live Demo

**Backend API**: https://car-classifier-tilhbeahgq-uc.a.run.app
**Frontend**: [Azure Static Web Apps URL after deployment]

### API Endpoints

- `GET /health` - Health check
- `POST /predict/body-type` - Classify vehicle type
- `POST /predict/brand` - Classify vehicle brand

## Training

Models trained on Kaggle using free GPU allocation. See `kaggle/README.md` for detailed instructions.

## Deployment

- **Backend**: Deployed to GCP Cloud Run via `backend/deploy.sh`
- **Frontend**: Automatically deployed via GitHub Actions to Azure Static Web Apps

## License

MIT License

## Author

Mission Ready Level 5 - Full Stack Developer Accelerator
Mission 1: AI-Powered Vehicle Classification System
