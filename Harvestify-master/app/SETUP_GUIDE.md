# AgriSmart Setup Guide

## Prerequisites
1. **Install Python 3.8+** from https://python.org/downloads/
   - ✅ Check "Add Python to PATH" during installation
   - ✅ Verify installation: `python --version`

## Installation Steps

### 1. Install Dependencies
Open Command Prompt in the app directory and run:

```bash
pip install Flask==2.3.3
pip install numpy==1.24.3
pip install pandas==2.0.3
pip install scikit-learn==1.3.0
pip install torch==2.0.1
pip install torchvision==0.15.2
pip install Pillow==10.0.0
pip install requests==2.31.0
pip install Werkzeug==2.3.7
```

Or install all at once:
```bash
pip install -r requirements_fixed.txt
```

### 2. Verify File Structure
Make sure these files exist:
- ✅ `models/plant_disease_model.pth`
- ✅ `models/RandomForest.pkl`
- ✅ `Data/fertilizer.csv`
- ✅ `config.py` (with weather API key)
- ✅ `utils/disease.py`
- ✅ `utils/fertilizer.py`
- ✅ `utils/model.py`

### 3. Run the Application

**Option 1: Use the fixed version (recommended)**
```bash
python app_fixed.py
```

**Option 2: Use the original version**
```bash
python app.py
```

### 4. Access the Application
Open your browser and go to: http://localhost:5000

## Features
- 🌱 **Crop Recommendation**: Get crop suggestions based on soil parameters
- 🧪 **Fertilizer Recommendation**: Get fertilizer suggestions for your crops
- 🔍 **Disease Detection**: Upload plant images to detect diseases

## Troubleshooting

### Common Issues:

1. **"Module not found" errors**
   - Install missing packages: `pip install <package_name>`

2. **Weather API not working**
   - Check internet connection
   - Verify API key in `config.py`

3. **Model loading errors**
   - Ensure model files exist in `models/` directory
   - Check file permissions

4. **Port already in use**
   - Change port in app.py: `app.run(port=5001)`

### File Locations:
- Models: `app/models/`
- Data: `app/Data/`
- Templates: `app/templates/`
- Static files: `app/static/`

## Notes
- The weather API key is already configured
- Models are pre-trained and ready to use
- Supports 38 different plant diseases
- Works with 22 different crops for recommendations