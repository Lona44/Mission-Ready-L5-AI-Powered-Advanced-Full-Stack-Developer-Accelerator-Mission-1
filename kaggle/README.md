# Kaggle Training Notebooks

This folder contains the Jupyter notebooks used to train the car classification models on Kaggle's free GPU platform.

## Notebooks

### Body Type Classification
**File**: `notebooks/body_type_classification_with_gradcam.ipynb`
- **Task**: Classify cars into 7 body types (Sedan, SUV, Pick-Up, Convertible, Coupe, Hatchback, VAN)
- **Model**: EfficientNetV2-Medium with ImageNet-21k pretraining
- **Dataset**: 7,549 images from [Cars Body Type Cropped](https://www.kaggle.com/datasets/ademboukhris/cars-body-type-cropped)
- **Results**: 97.63% test accuracy (exceeds 95% target)
- **Training Time**: ~2.5 hours on Kaggle P100 GPU

### Brand Classification
**File**: `notebooks/car_brand_classification_with_gradcam.ipynb`
- **Task**: Classify cars into 33 brands (Ram, Ford, BMW, etc.)
- **Model**: EfficientNetV2-Medium with ImageNet-21k pretraining
- **Dataset**: 16,467 images from [Car Brand Classification Dataset](https://www.kaggle.com/datasets/ahmedelsany/car-brand-classification-dataset)
- **Results**: 75.19% test accuracy (respectable for 33-class fine-grained classification)
- **Training Time**: ~2.5 hours on Kaggle P100 GPU

### Saved Outputs
**File**: `notebooks/car-brand-classification-with-gradcam.ipynb`
- Complete training run with all outputs, visualizations, and metrics
- Use this as reference for final results

## How to Run on Kaggle

### Prerequisites
1. Create a free [Kaggle account](https://www.kaggle.com)
2. Verify your account with a phone number (required for GPU access)

### Steps

1. **Upload Notebook**
   - Go to [Kaggle Notebooks](https://www.kaggle.com/code)
   - Click "New Notebook" → "Upload Notebook"
   - Upload one of the notebooks from this folder

2. **Add Dataset**
   - In the right sidebar, click "Add Data"
   - For body type: Search `ademboukhris/cars-body-type-cropped`
   - For brand: Search `ahmedelsany/car-brand-classification-dataset`
   - Click "Add"

3. **Enable GPU**
   - In the right sidebar under "Accelerator"
   - Select **"GPU P100"** or **"GPU T4 x2"**
   - This is critical - training will be very slow without GPU

4. **Run Training**
   - Click "Run All" or run cell by cell
   - Training takes 2-3 hours
   - Monitor validation accuracy in the progress output

5. **Download Models**
   After training completes, download from `/kaggle/working`:
   - `car_body_type_classifier.onnx` or `car_brand_classifier.onnx`
   - `class_labels_*.json`
   - `best_model_*.pth` (PyTorch checkpoint)
   - Training visualizations (optional but recommended)

6. **Save Models**
   Place downloaded files in the `models/` folder:
   ```
   models/
   ├── final/
   │   ├── car_body_type_classifier.onnx
   │   ├── car_brand_classifier.onnx
   │   ├── class_labels_body_type.json
   │   └── class_labels_brand.json
   └── checkpoints/
       ├── best_model_body_type.pth
       └── best_model_brand.pth
   ```

## Training Configuration

See `config/training_config.yaml` for hyperparameters used.

Key settings:
- **Optimizer**: AdamW
- **Learning Rate**: 1e-4
- **Batch Size**: 32
- **Image Size**: 224x224
- **Augmentation**: Horizontal flip, rotation, color jitter
- **Early Stopping**: Patience of 7 epochs

## Kaggle GPU Quota

Kaggle provides **30 hours/week** of free GPU time.
- Resets every Monday at 00:00 UTC
- Enough for ~10-15 training runs per week
- Check your quota at [Kaggle Settings](https://www.kaggle.com/settings)

## Model Outputs

After training, you'll have:
- **ONNX Model**: Optimized for deployment (used in GCP Cloud Run)
- **PyTorch Checkpoint**: Full model with optimizer state (for retraining)
- **Class Labels**: JSON mapping of class indices to names
- **Training History**: Loss and accuracy curves
- **Visualizations**: Confusion matrix, sample predictions, Grad-CAM heatmaps

## Grad-CAM Explainability

Both notebooks include Grad-CAM (Gradient-weighted Class Activation Mapping) to visualize what the model focuses on when making predictions. This is important for:
- **Transparency**: Insurance requirements for explainable AI
- **Debugging**: Identifying if model learned correct features
- **Trust**: Building confidence in model predictions

## Further Reading

- Full training guide: See `docs/KAGGLE_TRAINING_GUIDE.md` in project root
- Dataset analysis: See `docs/DATASET_ANALYSIS.md`
- Model performance: See `docs/PROJECT_STATUS.md`
