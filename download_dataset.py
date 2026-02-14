"""
Download Obesity Risk Classification dataset from Kaggle.
This script handles the download process.
"""

import os
import sys
from pathlib import Path
import subprocess

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def download_with_kaggle_api():
    """Try to download using Kaggle API."""
    try:
        # Check if kaggle is available
        result = subprocess.run(
            ["python3", "-m", "kaggle", "datasets", "download", 
             "-d", "fernandoramirez/obesity-risk-classification", 
             "-p", str(DATA_DIR)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Dataset downloaded successfully!")
            # Unzip if needed
            zip_files = list(DATA_DIR.glob("*.zip"))
            if zip_files:
                import zipfile
                for zip_file in zip_files:
                    print(f"Extracting {zip_file}...")
                    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                        zip_ref.extractall(DATA_DIR)
                    print(f"✅ Extracted to {DATA_DIR}")
            return True
        else:
            print(f"Kaggle API error: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error with Kaggle API: {e}")
        return False

def download_with_wget():
    """Try to download using wget (if public link available)."""
    # Note: Most Kaggle datasets require authentication
    # This is a placeholder for if we find a direct link
    print("Direct download not available - Kaggle requires authentication")
    return False

def main():
    print("=" * 60)
    print("Obesity Risk Classification Dataset Downloader")
    print("=" * 60)
    print()
    
    # Check if dataset already exists
    csv_files = list(DATA_DIR.glob("*.csv"))
    obesity_files = [f for f in csv_files if 'obesity' in f.name.lower() or 'risk' in f.name.lower()]
    
    if obesity_files:
        print(f"✅ Dataset already found: {obesity_files[0]}")
        return
    
    print("Attempting to download dataset...")
    print()
    
    # Try Kaggle API
    print("Method 1: Trying Kaggle API...")
    if download_with_kaggle_api():
        return
    
    print()
    print("=" * 60)
    print("Manual Download Required")
    print("=" * 60)
    print()
    print("The Kaggle API requires authentication.")
    print("Please download the dataset manually:")
    print()
    print("1. Go to: https://www.kaggle.com/datasets/fernandoramirez/obesity-risk-classification")
    print("2. Click 'Download' button")
    print("3. Extract the ZIP file")
    print("4. Place the CSV file in the 'data/' folder")
    print("5. Rename it to 'obesity_risk.csv' (optional)")
    print()
    print("Or set up Kaggle API:")
    print("1. Get API token from: https://www.kaggle.com/account")
    print("2. Place kaggle.json in ~/.kaggle/")
    print("3. Run this script again")
    print()

if __name__ == "__main__":
    main()
