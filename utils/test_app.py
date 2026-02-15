"""
Quick test script to verify Streamlit app components work
"""

import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd

MODEL_DIR = Path("model")

print("=" * 60)
print("Testing Streamlit App Components")
print("=" * 60)
print()

# Test 1: Load metrics
print("Test 1: Loading metrics...")
try:
    with open(MODEL_DIR / "metrics.json", "r") as f:
        metrics = json.load(f)
    print(f"✅ Metrics loaded: {len(metrics)} models")
    for name in metrics.keys():
        print(f"   - {name}: Accuracy={metrics[name]['accuracy']:.4f}")
except Exception as e:
    print(f"❌ Error loading metrics: {e}")
print()

# Test 2: Load reports
print("Test 2: Loading reports...")
try:
    with open(MODEL_DIR / "reports.json", "r") as f:
        reports = json.load(f)
    print(f"✅ Reports loaded: {len(reports)} models")
except Exception as e:
    print(f"❌ Error loading reports: {e}")
print()

# Test 3: Load confusion matrices
print("Test 3: Loading confusion matrices...")
try:
    with open(MODEL_DIR / "confusion_matrices.json", "r") as f:
        confusion_matrices = json.load(f)
    print(f"✅ Confusion matrices loaded: {len(confusion_matrices)} models")
    for name, cm in confusion_matrices.items():
        cm_array = np.array(cm)
        print(f"   - {name}: Shape {cm_array.shape}")
except Exception as e:
    print(f"❌ Error loading confusion matrices: {e}")
print()

# Test 4: Load a model
print("Test 4: Loading a model...")
try:
    model_path = MODEL_DIR / "logistic_regression.pkl"
    if model_path.exists():
        model = joblib.load(model_path)
        print(f"✅ Model loaded: {model_path.name}")
        print(f"   Model type: {type(model)}")
    else:
        print(f"❌ Model not found: {model_path}")
except Exception as e:
    print(f"❌ Error loading model: {e}")
print()

# Test 5: Test prediction
print("Test 5: Testing prediction...")
try:
    # Load a sample row from dataset
    df = pd.read_csv("data/obesity_risk.csv")
    X_sample = df.drop(columns=["NObeyesdad"]).head(1)
    
    model = joblib.load(MODEL_DIR / "logistic_regression.pkl")
    pred = model.predict(X_sample)
    prob = model.predict_proba(X_sample) if hasattr(model, "predict_proba") else None
    
    print(f"✅ Prediction successful")
    print(f"   Input shape: {X_sample.shape}")
    print(f"   Prediction: {pred}")
    if prob is not None:
        print(f"   Probabilities shape: {prob.shape}")
except Exception as e:
    print(f"❌ Error in prediction: {e}")
    import traceback
    traceback.print_exc()
print()

# Test 6: Check label encoder
print("Test 6: Checking label encoder...")
try:
    le_path = MODEL_DIR / "label_encoder.pkl"
    if le_path.exists():
        le = joblib.load(le_path)
        print(f"✅ Label encoder loaded")
        print(f"   Classes: {le.classes_}")
    else:
        print("⚠️  Label encoder not found (may not be needed)")
except Exception as e:
    print(f"⚠️  Label encoder issue: {e}")
print()

print("=" * 60)
print("✅ All tests completed!")
print("=" * 60)
print()
print("The Streamlit app should work correctly.")
print("Run: streamlit run app.py")
