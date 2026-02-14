import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.metrics import ConfusionMatrixDisplay, classification_report
import matplotlib.pyplot as plt

MODEL_DIR = Path("model")

st.set_page_config(page_title="Obesity Risk Classification", layout="wide")

st.title("Obesity Risk Classification - ML Assignment 2")

st.write(
    "This app compares multiple classification models on the Obesity Risk Classification dataset from Kaggle."
)

metrics_path = MODEL_DIR / "metrics.json"
reports_path = MODEL_DIR / "reports.json"
confusion_path = MODEL_DIR / "confusion_matrices.json"

if not metrics_path.exists():
    st.error("Models not found. Run train_models.py first.")
    st.stop()

with open(metrics_path, "r", encoding="utf-8") as f:
    metrics_table = json.load(f)

with open(reports_path, "r", encoding="utf-8") as f:
    reports = json.load(f)

with open(confusion_path, "r", encoding="utf-8") as f:
    confusion_matrices = json.load(f)

model_names = list(metrics_table.keys())

st.sidebar.header("Model Selection")
selected_model = st.sidebar.selectbox("Choose a model", model_names)

st.subheader("Evaluation Metrics")
metrics = metrics_table[selected_model]

col1, col2, col3 = st.columns(3)
col1.metric("Accuracy", f"{metrics['accuracy']:.4f}")
col1.metric("AUC", f"{metrics['auc']:.4f}")
col2.metric("Precision", f"{metrics['precision']:.4f}")
col2.metric("Recall", f"{metrics['recall']:.4f}")
col3.metric("F1 Score", f"{metrics['f1']:.4f}")
col3.metric("MCC", f"{metrics['mcc']:.4f}")

st.subheader("Confusion Matrix")
cm = np.array(confusion_matrices[selected_model])

# Try to load label encoder for class names
label_encoder_path = MODEL_DIR / "label_encoder.pkl"
if label_encoder_path.exists():
    try:
        le = joblib.load(label_encoder_path)
        class_names = le.classes_.tolist()
    except:
        # Fallback to generic labels
        n_classes = cm.shape[0]
        class_names = [f"Class {i}" for i in range(n_classes)]
else:
    # Fallback to generic labels
    n_classes = cm.shape[0]
    class_names = [f"Class {i}" for i in range(n_classes)]

fig, ax = plt.subplots(figsize=(8, 6))
ConfusionMatrixDisplay(cm, display_labels=class_names).plot(ax=ax, values_format="d")
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.subheader("Classification Report")
st.json(reports[selected_model])

st.subheader("Upload Test CSV for Predictions")

st.write(
    "Upload a CSV with the same feature columns as the dataset (excluding the target column)."
)

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    try:
        input_df = pd.read_csv(uploaded_file)
        
        # Remove target columns if present (common names)
        target_cols = [col for col in input_df.columns if any(word in col.lower() for word in 
            ['obesity', 'risk', 'class', 'category', 'target', 'label', 'income'])]
        if target_cols:
            input_df = input_df.drop(columns=target_cols)
            st.info(f"Removed target columns: {target_cols}")

        model_path = MODEL_DIR / f"{selected_model.replace(' ', '_').lower()}.pkl"
        if model_path.exists():
            model = joblib.load(model_path)
            preds = model.predict(input_df)
            probs = None
            if hasattr(model, "predict_proba"):
                probs = model.predict_proba(input_df)

            output = input_df.copy()
            
            # Decode predictions if label encoder exists
            label_encoder_path = MODEL_DIR / "label_encoder.pkl"
            if label_encoder_path.exists():
                try:
                    le = joblib.load(label_encoder_path)
                    output["prediction"] = le.inverse_transform(preds)
                except:
                    output["prediction"] = preds
            else:
                output["prediction"] = preds
            
            # Add probabilities
            if probs is not None:
                if probs.shape[1] == 2:
                    # Binary classification
                    output["probability_class_1"] = probs[:, 1]
                else:
                    # Multi-class: add probability for each class
                    for i in range(probs.shape[1]):
                        output[f"probability_class_{i}"] = probs[:, i]

            st.write("Predictions")
            st.dataframe(output.head(50))
            
            # Download option
            csv = output.to_csv(index=False)
            st.download_button(
                label="Download predictions as CSV",
                data=csv,
                file_name="predictions.csv",
                mime="text/csv"
            )
        else:
            st.error("Model file not found. Run train_models.py first.")
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        st.write("Please ensure the CSV file has the correct columns matching the dataset.")
        st.exception(e)

st.markdown("---")
st.caption("Built for ML Assignment 2 - BITS Virtual Lab")
