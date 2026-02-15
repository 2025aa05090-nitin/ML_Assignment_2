#!/bin/bash

# Setup and Run Script for ML Assignment 2 - Obesity Risk Classification

echo "============================================================"
echo "ML Assignment 2 - Obesity Risk Classification Setup"
echo "============================================================"
echo ""

DATA_DIR="data"
MODEL_DIR="model"

# Check if dataset exists
echo "Step 1: Checking for dataset..."
CSV_FILES=$(find $DATA_DIR -name "*.csv" -type f 2>/dev/null)
OBESITY_FILES=$(echo "$CSV_FILES" | grep -i "obesity\|risk" || echo "")

if [ -z "$OBESITY_FILES" ] && [ -z "$CSV_FILES" ]; then
    echo "❌ No dataset found in $DATA_DIR/"
    echo ""
    echo "Please download the dataset:"
    echo "1. Visit: https://www.kaggle.com/datasets/fernandoramirez/obesity-risk-classification"
    echo "2. Download and extract the ZIP file"
    echo "3. Place the CSV file in the 'data/' folder"
    echo ""
    echo "Or use Kaggle API (if configured):"
    echo "  kaggle datasets download -d fernandoramirez/obesity-risk-classification -p data/"
    echo ""
    exit 1
elif [ -z "$OBESITY_FILES" ]; then
    echo "✅ Found CSV file: $(echo $CSV_FILES | head -1)"
    DATASET_FILE=$(echo $CSV_FILES | head -1)
else
    echo "✅ Found obesity dataset: $(echo $OBESITY_FILES | head -1)"
    DATASET_FILE=$(echo $OBESITY_FILES | head -1)
fi

echo ""
echo "Step 2: Installing dependencies..."
pip install -q -r requirements.txt 2>/dev/null || {
    echo "⚠️  Some dependencies may need manual installation"
}

echo ""
echo "Step 3: Training models..."
echo "This may take 5-15 minutes depending on dataset size..."
echo ""

python3 train_models.py

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo "✅ Training Complete!"
    echo "============================================================"
    echo ""
    echo "Step 4: Updating README (optional)..."
    python3 UPDATE_README.py 2>/dev/null || echo "⚠️  Manual README update needed"
    echo ""
    echo "Step 5: Testing Streamlit app..."
    echo "Run: streamlit run app.py"
    echo ""
    echo "All done! Check model/metrics.json for results."
else
    echo ""
    echo "❌ Training failed. Check the error messages above."
    exit 1
fi
