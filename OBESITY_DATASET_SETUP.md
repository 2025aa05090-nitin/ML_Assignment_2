# Obesity Risk Classification Dataset - Setup Complete! ✅

## What Has Been Updated

### ✅ Code Files Updated

1. **`train_models.py`** - Completely rewritten for Obesity dataset
   - Automatically detects obesity dataset files
   - Identifies target column automatically
   - Handles both binary and multi-class classification
   - Supports all 6 required models
   - Calculates all 6 required metrics

2. **`app.py`** - Updated for Obesity dataset
   - Works with label encoder for class names
   - Handles multi-class predictions
   - Updated UI text for obesity classification

3. **Helper Files Created**:
   - `DATASET_INSTRUCTIONS.md` - How to download the dataset
   - `README_OBESITY_TEMPLATE.md` - Template for README
   - `UPDATE_README.py` - Script to auto-update README with metrics
   - `download_obesity_dataset.py` - Optional download script

## Next Steps to Complete Assignment

### Step 1: Download the Dataset (5-10 minutes)

**Option A: Using Kaggle API** (Recommended)
```bash
# Install Kaggle API
pip install kaggle

# Download dataset
kaggle datasets download -d fernandoramirez/obesity-risk-classification -p data/
cd data/
unzip obesity-risk-classification.zip
```

**Option B: Manual Download**
1. Go to: https://www.kaggle.com/datasets/fernandoramirez/obesity-risk-classification
2. Click "Download"
3. Extract ZIP file
4. Place CSV file in `data/` folder
5. Rename to `obesity_risk.csv` (optional)

### Step 2: Train All Models (10-15 minutes)

```bash
python3 train_models.py
```

This will:
- ✅ Load the obesity dataset
- ✅ Train all 6 models
- ✅ Calculate all 6 metrics (Accuracy, AUC, Precision, Recall, F1, MCC)
- ✅ Save models and metrics
- ✅ Generate confusion matrices

**Expected Output:**
- Training progress for each model
- Performance summary at the end
- Models saved in `model/` directory

### Step 3: Update README.md (5 minutes)

After training, you have two options:

**Option A: Manual Update**
1. Copy metrics from `model/metrics.json`
2. Update `README.md` with:
   - Actual dataset statistics (rows, features)
   - Comparison table with metrics
   - Observations for each model

**Option B: Auto-Update (Partial)**
```bash
python3 UPDATE_README.py
```
This updates the comparison table automatically, but you still need to:
- Update dataset description with actual numbers
- Write observations for each model

### Step 4: Test Streamlit App (5 minutes)

```bash
streamlit run app.py
```

Verify:
- ✅ All 6 models appear in dropdown
- ✅ Metrics display correctly
- ✅ Confusion matrix shows
- ✅ CSV upload works
- ✅ Predictions generate correctly

### Step 5: Verify Requirements Met

Check that your dataset meets assignment requirements:
- ✅ **Minimum 12 features** (excluding target)
- ✅ **Minimum 500 instances**
- ✅ **All 6 models trained**
- ✅ **All 6 metrics calculated**

The training script will warn you if requirements aren't met.

## File Structure

```
ML_assignment/
├── data/
│   └── obesity_risk.csv          # Dataset (you need to download)
├── model/
│   ├── *.pkl                     # Trained models (generated)
│   ├── metrics.json              # All metrics (generated)
│   ├── reports.json              # Classification reports (generated)
│   └── confusion_matrices.json   # Confusion matrices (generated)
├── train_models.py               # Training script (updated)
├── app.py                        # Streamlit app (updated)
├── README.md                     # Documentation (needs update after training)
├── requirements.txt              # Dependencies
└── DATASET_INSTRUCTIONS.md       # Download instructions
```

## Troubleshooting

### "Dataset not found" error?
- Make sure CSV file is in `data/` folder
- Check filename matches: `obesity_risk.csv`, `ObesityDataSet.csv`, etc.
- Or place any CSV file in `data/` and script will use it

### "Not enough features" warning?
- Assignment requires minimum 12 features
- Check your dataset has enough columns (excluding target)
- You may need feature engineering or a different dataset

### "Not enough instances" warning?
- Assignment requires minimum 500 rows
- Check your dataset has enough rows
- Filter out missing data if needed

### Models not training?
- Check all dependencies installed: `pip install -r requirements.txt`
- Verify dataset is valid CSV
- Check for missing values in critical columns

### Streamlit app errors?
- Make sure models are trained first: `python3 train_models.py`
- Check `model/` directory has all files
- Verify `metrics.json` exists

## Quick Start Commands

```bash
# 1. Download dataset (if using Kaggle API)
kaggle datasets download -d fernandoramirez/obesity-risk-classification -p data/
cd data/ && unzip *.zip && cd ..

# 2. Train models
python3 train_models.py

# 3. Update README (optional auto-update)
python3 UPDATE_README.py

# 4. Test app
streamlit run app.py

# 5. Check metrics
cat model/metrics.json
```

## Assignment Checklist

Before submission, ensure:

- [ ] Dataset downloaded and in `data/` folder
- [ ] All 6 models trained successfully
- [ ] All 6 metrics calculated and saved
- [ ] README.md updated with:
  - [ ] Dataset description (actual numbers)
  - [ ] Comparison table (all metrics)
  - [ ] Observations for each model
- [ ] Streamlit app tested and working
- [ ] All requirements met (12+ features, 500+ instances)

## Need Help?

- See `DATASET_INSTRUCTIONS.md` for detailed download instructions
- Check training output for warnings or errors
- Verify `model/metrics.json` contains all metrics
- Test app locally before deployment

---

**You're all set!** Download the dataset, run training, update README, and you're ready for submission! 🚀
