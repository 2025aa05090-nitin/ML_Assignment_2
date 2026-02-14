"""
Script to download Obesity Risk Classification dataset from Kaggle.
Make sure you have kaggle API set up:
1. Install: pip install kaggle
2. Get API token from https://www.kaggle.com/account
3. Place kaggle.json in ~/.kaggle/
"""

import os
from pathlib import Path
import pandas as pd

# Common Obesity Risk Classification dataset names on Kaggle
OBESITY_DATASETS = [
    "fernandoramirez/obesity-risk-classification",
    "sujithmandala/obesity-risk-classification",
    "mariacamilacastroc/obesity-risk-classification",
]

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def download_from_kaggle(dataset_name: str):
    """Download dataset from Kaggle using kaggle API."""
    try:
        import kaggle
        from kaggle.api.kaggle_api_extended import KaggleApi
        
        api = KaggleApi()
        api.authenticate()
        
        print(f"Downloading dataset: {dataset_name}")
        api.dataset_download_files(dataset_name, path=DATA_DIR, unzip=True)
        print("Download complete!")
        return True
    except Exception as e:
        print(f"Error downloading from Kaggle: {e}")
        print("\nAlternative: Please download manually from Kaggle and place in data/ folder")
        return False

def find_obesity_csv():
    """Find the obesity dataset CSV file in data directory."""
    csv_files = list(DATA_DIR.glob("*.csv"))
    if csv_files:
        # Look for files with 'obesity' in name
        obesity_files = [f for f in csv_files if 'obesity' in f.name.lower() or 'risk' in f.name.lower()]
        if obesity_files:
            return obesity_files[0]
        return csv_files[0]  # Return first CSV if no specific match
    return None

def inspect_dataset(csv_path: Path):
    """Inspect the dataset structure."""
    print(f"\nInspecting dataset: {csv_path}")
    df = pd.read_csv(csv_path)
    
    print(f"\nDataset shape: {df.shape}")
    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    print(f"\nColumn names:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col}")
    
    print(f"\nFirst few rows:")
    print(df.head())
    
    print(f"\nData types:")
    print(df.dtypes)
    
    print(f"\nMissing values:")
    print(df.isnull().sum())
    
    # Try to identify target column
    target_candidates = [col for col in df.columns if any(word in col.lower() for word in ['obesity', 'risk', 'class', 'target', 'label', 'category'])]
    if target_candidates:
        print(f"\nPossible target columns: {target_candidates}")
    
    return df

if __name__ == "__main__":
    print("=" * 60)
    print("Obesity Risk Classification Dataset Downloader")
    print("=" * 60)
    
    # Try to download from Kaggle
    downloaded = False
    for dataset in OBESITY_DATASETS:
        if download_from_kaggle(dataset):
            downloaded = True
            break
    
    # Find the CSV file
    csv_file = find_obesity_csv()
    
    if csv_file:
        print(f"\nFound dataset file: {csv_file}")
        df = inspect_dataset(csv_file)
        
        # Save as standard name
        output_path = DATA_DIR / "obesity_risk.csv"
        df.to_csv(output_path, index=False)
        print(f"\nDataset saved as: {output_path}")
    else:
        print("\nNo CSV file found. Please:")
        print("1. Download the dataset from Kaggle manually")
        print("2. Place the CSV file in the data/ folder")
        print("3. Or use kaggle API: pip install kaggle")
