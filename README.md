# Car Vision Classification Project

AI-powered vehicle type classification system using state-of-the-art deep learning models, deployed on Azure.

## Overview

This project builds an end-to-end vehicle classification system that can accurately categorize cars into types (Sedan, SUV, Truck, etc.). The system uses modern computer vision models trained on Kaggle and deployed on Microsoft Azure.

## Project Goals

- Achieve 95%+ accuracy on vehicle classification
- Train using state-of-the-art models (EfficientNet V2 / ConvNeXt V2)
- Deploy as production-ready Azure ML endpoint
- Create professional web application for demonstrations
- Build comprehensive portfolio piece

## Technology Stack

### Training
- **Platform**: Kaggle (free GPU access)
- **Framework**: PyTorch with timm library
- **Models**: EfficientNet V2, ConvNeXt V2, or Swin Transformer V2
- **Dataset**: Car Body Types Images Dataset (7,000 images)

### Deployment
- **Cloud**: Microsoft Azure Machine Learning
- **Model Format**: ONNX
- **API**: REST endpoint

### Web Application
- **Frontend**: React + Vite
- **Styling**: TailwindCSS (or your choice)
- **API Integration**: Azure ML REST API

## Project Structure

```
Mission_01/
├── data/              # Dataset storage
├── notebooks/         # Jupyter notebooks for training
├── models/            # Trained model artifacts
├── src/               # Python source code
├── azure/             # Azure deployment scripts
├── webapp/            # React web application
├── docs/              # Documentation
└── config/            # Configuration files
```

## Getting Started

### Prerequisites
- Python 3.9+
- Kaggle account and API credentials
- Azure account with free credits
- Node.js 18+ (for React app)

### Setup

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Kaggle API**
   - Place `kaggle.json` in `~/.kaggle/`
   - Set permissions: `chmod 600 ~/.kaggle/kaggle.json`

3. **Download dataset**
   ```bash
   kaggle datasets download -d ademboukhris/cars-body-type-cropped
   ```

## Workflow

1. **Data Preparation** → Explore and preprocess dataset
2. **Model Training** → Train on Kaggle with free GPU
3. **Model Export** → Convert to ONNX format
4. **Azure Deployment** → Deploy as ML endpoint
5. **Web App** → Build React interface
6. **Testing** → End-to-end validation

## Current Status

🚧 Project in development

- [ ] Data downloaded and explored
- [ ] Model training notebook created
- [ ] Model trained (target: 95%+ accuracy)
- [ ] Model exported to ONNX
- [ ] Azure endpoint deployed
- [ ] React web app built
- [ ] End-to-end testing complete

## License

MIT License - See LICENSE file for details

## Author

Mission Ready L5 - Advanced AI Project
