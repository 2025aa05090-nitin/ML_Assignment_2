# Dataset Download Instructions - Obesity Risk Classification

## Step 1: Download the Dataset from Kaggle

### Option A: Using Kaggle API (Recommended)

1. **Install Kaggle API**:
   ```bash
   pip install kaggle
   ```

2. **Get your Kaggle API credentials**:
   - Go to https://www.kaggle.com/account
   - Scroll to "API" section
   - Click "Create New Token"
   - This downloads `kaggle.json` file

3. **Set up credentials**:
   ```bash
   mkdir -p ~/.kaggle
   mv ~/Downloads/kaggle.json ~/.kaggle/
   chmod 600 ~/.kaggle/kaggle.json
   ```

4. **Download the dataset**:
   ```bash
   kaggle datasets download -d fernandoramirez/obesity-risk-classification -p data/
   cd data/
   unzip obesity-risk-classification.zip
   ```

### Option B: Manual Download

1. **Go to Kaggle**:
   - Visit: https://www.kaggle.com/datasets/fernandoramirez/obesity-risk-classification
   - Or search for "Obesity Risk Classification" on Kaggle

2. **Download the dataset**:
   - Click "Download" button
   - Extract the ZIP file
   - Place the CSV file in the `data/` folder

3. **Rename the file** (optional but recommended):
   ```bash
   mv data/ObesityDataSet.csv data/obesity_risk.csv
   ```

## Step 2: Verify Dataset

The dataset should have:
- **Minimum 12 features** (excluding target)
- **Minimum 500 instances**
- A target column (usually named: `NObeyesdad`, `Obesity`, `Risk`, or similar)

Common features in obesity datasets:
- Age, Gender, Height, Weight, BMI
- Family history
- Physical activity levels
- Eating habits
- Transportation used
- etc.

## Step 3: Run Training

Once the dataset is in place:

```bash
python3 train_models.py
```

The script will:
- Automatically detect the dataset
- Identify the target column
- Train all 6 models
- Generate metrics and save models

## Troubleshooting

### Dataset not found?
- Make sure the CSV file is in the `data/` folder
- Check filename matches one of: `obesity_risk.csv`, `ObesityDataSet.csv`, `obesity.csv`, `Obesity_Risk_Classification.csv`
- Or place any CSV file in `data/` folder and the script will use it

### Wrong target column?
- The script automatically detects target columns
- If wrong, you can manually specify in the code
- Look for columns with names containing: 'obesity', 'risk', 'class', 'category', 'target', 'label'

### Not enough features?
- Assignment requires minimum 12 features
- If your dataset has fewer, you may need feature engineering
- Or use a different obesity dataset with more features

## Alternative Datasets

If the main dataset doesn't work, try these alternatives on Kaggle:
1. Search: "obesity classification"
2. Search: "obesity prediction"
3. Search: "obesity risk factors"

Make sure any alternative has:
- At least 12 features
- At least 500 rows
- Classification target variable
