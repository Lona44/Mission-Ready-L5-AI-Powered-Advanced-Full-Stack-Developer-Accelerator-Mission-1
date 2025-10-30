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
- **Accuracy**: 75.2% on test set (76.9% validation)
- **Architecture**: EfficientNetV2-Medium (ImageNet-21k pretrained)
- **Dataset**: 16,467 images

## Why EfficientNetV2?

**EfficientNetV2** (Tan & Le, 2021) represents a breakthrough in efficient computer vision, developed by Google Research Brain Team and published at ICML 2021.

### State-of-the-Art Performance
- Achieves **87.3% top-1 accuracy** on ImageNet when pretrained on ImageNet-21k
- Trains **5-11x faster** than Vision Transformers while being **6.8x smaller**
- Outperforms previous state-of-the-art CNNs on ImageNet, CIFAR, Cars, and Flowers datasets

### Key Innovations
- **Training-Aware NAS**: Jointly optimizes accuracy, model size, and training speed
- **Fused-MBConv**: Accelerator-friendly operations for faster inference
- **Progressive Learning**: Adaptive regularization during training for optimal accuracy

### Why It's Ideal for This Project
- **Efficiency**: Fast training on free Kaggle GPUs (~2.5 hours per model)
- **Accuracy**: High performance on fine-grained classification tasks
- **Deployment**: Compact model size enables serverless deployment on Cloud Run
- **Transfer Learning**: Excellent ImageNet-21k pretraining for vehicle features

**Reference**: Tan, M., & Le, Q. V. (2021). EfficientNetV2: Smaller Models and Faster Training. ICML 2021.

## Technology Stack

### Training
- **Platform**: Kaggle Notebooks (Tesla P100 GPU)
- **Framework**: PyTorch 2.x + TIMM
- **Model**: `tf_efficientnetv2_m.in21k_ft_in1k`
- **Training Time**: ~2.5 hours per model
- **Notebooks**:
  - [Body Type Classification with Grad-CAM](https://www.kaggle.com/code/maalona/body-type-classification-with-gradcam)
  - [Brand Classification with Grad-CAM](https://www.kaggle.com/code/maalona/car-brand-classification-with-gradcam)

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

Models trained on Kaggle using free GPU allocation (Tesla P100). Training notebooks available on Kaggle:

- [Body Type Classification with Grad-CAM](https://www.kaggle.com/code/maalona/body-type-classification-with-gradcam) - 97.6% test accuracy
- [Brand Classification with Grad-CAM](https://www.kaggle.com/code/maalona/car-brand-classification-with-gradcam) - 75.2% test accuracy

See `kaggle/README.md` for detailed instructions on running these notebooks.

## Deployment

- **Backend**: Deployed to GCP Cloud Run via `backend/deploy.sh`
- **Frontend**: Automatically deployed via GitHub Actions to Azure Static Web Apps

## License

MIT License

## Author

Mission Ready Level 5 - Full Stack Developer Accelerator
Mission 1: AI-Powered Vehicle Classification System
