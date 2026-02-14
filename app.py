import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import confusion_matrix

# --- Page Configuration ---
st.set_page_config(
    page_title="Obesity Risk Predictor 🚀",
    page_icon="🥑",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS for "Playful" Theme ---
st.markdown(
    """
    <style>
    /* Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Colorful Headers */
    h1 {
        color: #FF6B6B;
        font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
        text-align: center;
        text-shadow: 2px 2px 4px #00000020;
    }
    h2, h3 {
        color: #4ECDC4;
        font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
    }
    
    /* Fun Buttons */
    .stButton>button {
        background-color: #FF6B6B;
        color: white;
        border-radius: 20px;
        border: 2px solid #FF6B6B;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #FF8787;
        border-color: #FF8787;
        transform: scale(1.05);
    }
    
    /* Custom Metric Cards */
    div[data-testid="stMetricValue"] {
        color: #1A535C;
        font-weight: bold;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #FFE66D;
        background-image: linear-gradient(315deg, #FFE66D 0%, #FF6B6B 74%);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

MODEL_DIR = Path("model")

# --- Header Section ---
st.title("🥑 Obesity Risk Predictor 🚀")
st.markdown(
    """
    <h3 style='text-align: center; color: #1A535C;'>
    Let's find out what the AI thinks! 🤖✨
    </h3>
    """,
    unsafe_allow_html=True,
)
st.markdown("---")

# --- Load Data & Models ---
metrics_path = MODEL_DIR / "metrics.json"
reports_path = MODEL_DIR / "reports.json"
confusion_path = MODEL_DIR / "confusion_matrices.json"

if not metrics_path.exists():
    st.error("❌ Whoops! Models not found. Please run `train_models.py` first! 🏃‍♂️")
    st.stop()

with open(metrics_path, "r", encoding="utf-8") as f:
    metrics_table = json.load(f)

with open(reports_path, "r", encoding="utf-8") as f:
    reports = json.load(f)

with open(confusion_path, "r", encoding="utf-8") as f:
    confusion_matrices = json.load(f)

model_names = list(metrics_table.keys())

# --- Sidebar ---
with st.sidebar:
    st.header("🎮 Control Panel")
    st.markdown("Choose your champion model below! 👇")
    selected_model = st.selectbox("🤖 Select Model", model_names)
    
    st.markdown("---")
    st.info("💡 **Did you know?**\nHealthy eating and exercise are key! 🍎🧘‍♀️")
    st.markdown("Created with ❤️ for ML Assignment 2")

# --- Main Content ---

# 1. Metrics Display
st.subheader(f"📊 Performance: {selected_model}")
metrics = metrics_table[selected_model]

col1, col2, col3, col4 = st.columns(4)
col1.metric("🎯 Accuracy", f"{metrics['accuracy']:.2%}")
col2.metric("📈 AUC Score", f"{metrics['auc']:.4f}")
col3.metric("⚖️ F1 Score", f"{metrics['f1']:.4f}")
col4.metric("🤝 MCC", f"{metrics['mcc']:.4f}")

# 2. Confusion Matrix (Interactive Plotly Heatmap)
st.subheader("🧩 Confusion Matrix")
cm = np.array(confusion_matrices[selected_model])

# Try to load label encoder for class names
label_encoder_path = MODEL_DIR / "label_encoder.pkl"
class_names = [f"Class {i}" for i in range(cm.shape[0])]
if label_encoder_path.exists():
    try:
        le = joblib.load(label_encoder_path)
        class_names = le.classes_.tolist()
    except:
        pass

fig_cm = px.imshow(
    cm,
    text_auto=True,
    labels=dict(x="Predicted", y="Actual", color="Count"),
    x=class_names,
    y=class_names,
    color_continuous_scale="Viridis",
    aspect="auto",
)
fig_cm.update_layout(title_text=f"How well did {selected_model} do?", title_x=0.5)
st.plotly_chart(fig_cm, use_container_width=True)

# 3. Model Comparison Chart
with st.expander("🏆 See how models compare against each other!"):
    accuracies = {model: m['accuracy'] for model, m in metrics_table.items()}
    fig_comp = px.bar(
        x=list(accuracies.keys()),
        y=list(accuracies.values()),
        color=list(accuracies.values()),
        labels={'x': 'Model', 'y': 'Accuracy', 'color': 'Accuracy'},
        title="Model Accuracy Showdown 🥊",
        color_continuous_scale="Plasma"
    )
    st.plotly_chart(fig_comp, use_container_width=True)

# 4. Predictions Section
st.markdown("---")
st.subheader("🔮 Make a Prediction!")
st.markdown(
    """
    Upload your CSV file here, and watch the magic happen! ✨
    *(Ensure columns match the training data)*
    """
)

uploaded_file = st.file_uploader("📂 Upload CSV File", type=["csv"])

if uploaded_file is not None:
    try:
        input_df = pd.read_csv(uploaded_file)
        
        # Remove target columns if present
        target_cols = [col for col in input_df.columns if any(word in col.lower() for word in 
            ['obesity', 'risk', 'class', 'category', 'target', 'label', 'income'])]
        if target_cols:
            input_df = input_df.drop(columns=target_cols)
            st.success(f"🧹 Cleaned up target columns: {target_cols}")

        model_path = MODEL_DIR / f"{selected_model.replace(' ', '_').lower()}.pkl"
        if model_path.exists():
            model = joblib.load(model_path)
            preds = model.predict(input_df)
            probs = None
            if hasattr(model, "predict_proba"):
                probs = model.predict_proba(input_df)

            output = input_df.copy()
            
            # Decode predictions
            if label_encoder_path.exists():
                try:
                    le = joblib.load(label_encoder_path)
                    output["Predicted_Class"] = le.inverse_transform(preds)
                except:
                    output["Predicted_Class"] = preds
            else:
                output["Predicted_Class"] = preds
            
            # Show results with styling
            st.balloons()  # Fun effect!
            st.markdown("### 🎉 Prediction Results")
            
            # Highlight predictions
            def highlight_cols(s):
                if s.name == 'Predicted_Class':
                    return ['background-color: #FFE66D; color: black']*len(s)
                return ['']*len(s)

            st.dataframe(output.style.apply(highlight_cols, axis=0))
            
            # Download button
            csv = output.to_csv(index=False)
            st.download_button(
                label="📥 Download Predictions",
                data=csv,
                file_name="my_predictions.csv",
                mime="text/csv"
            )
        else:
            st.error("🚫 Model file missing!")
    except Exception as e:
        st.error(f"⚠️ Oops! Something went wrong: {str(e)}")

