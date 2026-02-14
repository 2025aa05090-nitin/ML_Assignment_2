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
    initial_sidebar_state="collapsed", # Collapse sidebar to save space
)

# --- Custom CSS for "Compact & Playful" Theme ---
st.markdown(
    """
    <style>
    /* Gradient Background - Subtle */
    .stApp {
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
    }

    /* FORCE ALL TEXT TO BE DARK */
    .stApp, .stApp p, .stApp div, .stApp span, .stApp label, .stApp li {
        color: #000000 !important;
        font-size: 0.9rem !important; /* Slightly smaller text */
    }

    /* Compact Padding */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    /* Colorful Headers - High Contrast & Compact */
    h1 {
        color: #c0392b !important;
        font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
        text-align: center;
        text-shadow: 1px 1px 2px #00000020;
        font-size: 2rem !important; /* Smaller Title */
        margin-bottom: 0.5rem !important;
    }
    h2, h3 {
        color: #27ae60 !important;
        font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
        font-weight: 700;
        font-size: 1.2rem !important; /* Smaller Subheaders */
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Fun Buttons - High Contrast */
    .stButton>button {
        background-color: #e74c3c !important;
        color: white !important;
        border-radius: 15px;
        border: 2px solid #c0392b !important;
        font-weight: bold;
        transition: all 0.3s ease;
        padding: 0.2rem 1rem !important;
        height: auto !important;
    }
    .stButton>button:hover {
        background-color: #c0392b !important;
        border-color: #c0392b !important;
        transform: scale(1.05);
    }
    .stButton>button:hover p {
        color: white !important;
    }

    /* Custom Metric Cards */
    div[data-testid="stMetricValue"] {
        color: #2c3e50 !important;
        font-weight: 800;
        font-size: 1.5rem !important; /* Compact Metrics */
    }
    div[data-testid="stMetricLabel"] {
        color: #34495e !important;
        font-weight: 600;
        font-size: 0.8rem !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #f39c12;
        background-image: linear-gradient(315deg, #f39c12 0%, #d35400 74%);
    }
    section[data-testid="stSidebar"] * {
        color: #2c3e50 !important;
    }
    
    /* Input fields text color */
    input {
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

MODEL_DIR = Path("model")

# --- Load Data & Models ---
metrics_path = MODEL_DIR / "metrics.json"
reports_path = MODEL_DIR / "reports.json"
confusion_path = MODEL_DIR / "confusion_matrices.json"

if not metrics_path.exists():
    st.error("❌ Models not found. Run `train_models.py` first!")
    st.stop()

with open(metrics_path, "r", encoding="utf-8") as f:
    metrics_table = json.load(f)

with open(reports_path, "r", encoding="utf-8") as f:
    reports = json.load(f)

with open(confusion_path, "r", encoding="utf-8") as f:
    confusion_matrices = json.load(f)

model_names = list(metrics_table.keys())

# --- Top Models Control (Moved from Sidebar for Single Page Feel) ---
c1, c2 = st.columns([3, 1])
with c1:
    st.markdown("<h1 style='text-align: left;'>🥑 Obesity Risk Predictor 🚀</h1>", unsafe_allow_html=True)
with c2:
    selected_model = st.selectbox("🤖 Change Model", model_names, label_visibility="collapsed")


# --- Main Content Grid ---

# Row 1: Metrics (Very Compact)
metrics = metrics_table[selected_model]
m1, m2, m3, m4 = st.columns(4)
m1.metric("🎯 Accuracy", f"{metrics['accuracy']:.1%}")
m2.metric("📈 AUC", f"{metrics['auc']:.3f}")
m3.metric("⚖️ F1", f"{metrics['f1']:.3f}")
m4.metric("🤝 MCC", f"{metrics['mcc']:.3f}")

st.markdown("---", unsafe_allow_html=True)

# Row 2: Split Views (Confusion Matrix | Predictions)
col_left, col_right = st.columns([1, 1], gap="medium")

with col_left:
    st.subheader(f"🧩 Confusion Matrix: {selected_model}")
    cm = np.array(confusion_matrices[selected_model])
    
    # Try to load label encoder for class names
    label_encoder_path = MODEL_DIR / "label_encoder.pkl"
    class_names = [f"C{i}" for i in range(cm.shape[0])] # Short names by default
    if label_encoder_path.exists():
        try:
            le = joblib.load(label_encoder_path)
            # Shorten names for compact view
            class_names = [name[:10]+".." if len(name)>10 else name for name in le.classes_.tolist()]
        except:
            pass

    fig_cm = px.imshow(
        cm,
        text_auto=True,
        labels=dict(x="Pred", y="True", color="Cnt"),
        x=class_names,
        y=class_names,
        color_continuous_scale="Viridis",
        aspect="auto",
        height=350, # Fixed height to fit screen
    )
    fig_cm.update_layout(margin=dict(l=0, r=0, t=20, b=0))
    st.plotly_chart(fig_cm, use_container_width=True)

    with st.expander("🏆 Model Comparison"):
        accuracies = {model: m['accuracy'] for model, m in metrics_table.items()}
        fig_comp = px.bar(
            x=list(accuracies.values()),
            y=list(accuracies.keys()),
            orientation='h',
            labels={'x': 'Acc', 'y': ''},
            title="Accuracy Leaderboard",
            color_continuous_scale="Plasma",
            height=200
        )
        fig_comp.update_layout(margin=dict(l=0, r=0, t=30, b=0))
        st.plotly_chart(fig_comp, use_container_width=True)

with col_right:
    st.subheader("🔮 Rapid Prediction")
    st.info("Upload CSV to predict! 📂")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")

    if uploaded_file is not None:
        try:
            input_df = pd.read_csv(uploaded_file)
            
            # Remove target columns if present
            target_cols = [col for col in input_df.columns if any(word in col.lower() for word in 
                ['obesity', 'risk', 'class', 'category', 'target', 'label', 'income'])]
            if target_cols:
                input_df = input_df.drop(columns=target_cols)

            model_path = MODEL_DIR / f"{selected_model.replace(' ', '_').lower()}.pkl"
            if model_path.exists():
                model = joblib.load(model_path)
                preds = model.predict(input_df)

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
                
                # Show results compactly
                st.success("Analysis Complete! 🎉")
                
                # Highlight predictions
                def highlight_cols(s):
                    if s.name == 'Predicted_Class':
                        return ['background-color: #FFE66D; color: black']*len(s)
                    return ['']*len(s)

                st.dataframe(output.style.apply(highlight_cols, axis=0), height=200)
                
                # Download button
                csv = output.to_csv(index=False)
                st.download_button(
                    label="📥 Download Results",
                    data=csv,
                    file_name="predictions.csv",
                    mime="text/csv"
                )
            else:
                st.error("🚫 Model missing!")
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)[:50]}...")

