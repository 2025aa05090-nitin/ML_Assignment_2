import json
import pickle
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
    initial_sidebar_state="expanded", # Expand sidebar for controls
)

# --- Custom CSS for "Clean & Friendly" Theme ---
st.markdown(
    """
    <style>
    /* Gradient Background - Subtle & Fresh */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    /* Force Dark Text for Readability */
    .stApp, .stApp p, .stApp div, .stApp span, .stApp label, .stApp li, h1, h2, h3, h4, h5, h6 {
        color: #2c3e50 !important;
        font-family: 'Roboto', 'Helvetica Neue', 'Arial', sans-serif !important;
    }

    /* Compact Padding */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    /* Modern Headers */
    h1 {
        color: #e74c3c !important; /* Accent Red */
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.2rem !important;
        font-size: 2.2rem !important;
    }
    h2, h3 {
        color: #27ae60 !important; /* Accent Green */
        font-weight: 600;
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Card-like Styling for Metrics */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        color: #2c3e50 !important;
        font-weight: 700;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.9rem !important;
        color: #7f8c8d !important;
    }

    /* Sidebar Styling - Distinct */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #ddd;
    }
    section[data-testid="stSidebar"] h1 {
        font-size: 1.5rem !important;
        text-align: left;
    }

    /* Input Fields & Buttons */
    .stButton>button {
        background-color: #3498db !important;
        color: white !important;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        transition: 0.2s;
    }
    .stButton>button:hover {
        background-color: #2980b9 !important;
        color: white !important; 
    }
    div[data-baseweb="select"] > div {
        background-color: white !important;
        color: black !important;
        border-radius: 8px;
    }
    
    /* FIX DROPDOWN VISIBILITY */
    div[data-baseweb="popover"], div[data-baseweb="menu"], div[role="listbox"] {
        background-color: white !important;
        color: black !important;
        border: 1px solid #eee;
    }
    div[data-baseweb="option"] {
        color: black !important;
    }
    div[aria-selected="true"] {
        background-color: #f1f2f6 !important;
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
    st.error("Models not found. Run `train_models.py` first.")
    st.stop()

with open(metrics_path, "r", encoding="utf-8") as f:
    metrics_table = json.load(f)

with open(reports_path, "r", encoding="utf-8") as f:
    reports = json.load(f)

with open(confusion_path, "r", encoding="utf-8") as f:
    confusion_matrices = json.load(f)

model_names = list(metrics_table.keys())

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.title("🎛️ Control Panel")
    
    st.markdown("### 1. Choose Model")
    selected_model = st.selectbox("Select Model", model_names, label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("### 2. Predict New Data")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    
    st.markdown("---")
    st.info("💡 **Tip:** Use the sidebar to switch models or upload data without scrolling!")


# --- MAIN CONTENT ---

# Title area
st.markdown("<h1>🥑 Obesity Risk Predictor 🚀</h1>", unsafe_allow_html=True)

# Metrics Row
metrics = metrics_table[selected_model]
m1, m2, m3, m4 = st.columns(4)
m1.metric("Accuracy", f"{metrics['accuracy']:.1%}")
m2.metric("AUC Score", f"{metrics['auc']:.3f}")
m3.metric("F1 Score", f"{metrics['f1']:.3f}")
m4.metric("MCC Score", f"{metrics['mcc']:.3f}")

st.markdown("---", unsafe_allow_html=True)

# Comparison Row
col_left, col_right = st.columns([1, 1], gap="medium")

with col_left:
    st.subheader(f"Confusion Matrix: {selected_model}")
    cm = np.array(confusion_matrices[selected_model])
    
    # Load labels
    label_encoder_path = MODEL_DIR / "label_encoder.pkl"
    class_names = [f"C{i}" for i in range(cm.shape[0])]
    if label_encoder_path.exists():
        try:
            le = joblib.load(label_encoder_path)
            # Truncate long names for layout
            class_names = [name[:12]+".." if len(name)>12 else name for name in le.classes_.tolist()]
        except:
            pass

    fig_cm = px.imshow(
        cm,
        text_auto=True,
        labels=dict(x="Pred", y="True", color="Cnt"),
        x=class_names,
        y=class_names,
        color_continuous_scale="Blues", # Clean blue scale
        aspect="auto",
        height=350,
    )
    fig_cm.update_layout(
        margin=dict(l=0, r=0, t=20, b=0),
        template="plotly_white",
        font=dict(color="#2c3e50", family="Roboto"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_cm, use_container_width=True, theme=None)

with col_right:
    # If file uploaded, show predictions here. Else show Comparison
    if uploaded_file is not None:
        st.subheader("🔮 Prediction Results")
        try:
            input_df = pd.read_csv(uploaded_file)
            
            # Remove target columns
            target_cols = [col for col in input_df.columns if any(word in col.lower() for word in 
                ['obesity', 'risk', 'class', 'category', 'target', 'label', 'income'])]
            if target_cols:
                input_df = input_df.drop(columns=target_cols)

            model_path = MODEL_DIR / f"{selected_model.replace(' ', '_').lower()}.pkl"
            if model_path.exists():
                with open(model_path, "rb") as f:
                    model = pickle.load(f)
                preds = model.predict(input_df)

                output = input_df.copy()
                if label_encoder_path.exists():
                    try:
                        le = joblib.load(label_encoder_path)
                        output["Predicted_Class"] = le.inverse_transform(preds)
                    except:
                        output["Predicted_Class"] = preds
                else:
                    output["Predicted_Class"] = preds
                
                # Check for single prediction vs batch for display
                if len(output) < 5:
                    st.success("Predictions Ready!")
                
                # Highlight
                def highlight_cols(s):
                    if s.name == 'Predicted_Class':
                        return ['background-color: #dff9fb; color: #2c3e50; font-weight: bold']*len(s)
                    return ['']*len(s)

                st.dataframe(output.style.apply(highlight_cols, axis=0), height=250)
                
                csv = output.to_csv(index=False)
                st.download_button("📥 Download Results", csv, "predictions.csv", "text/csv")
            else:
                st.error("Model missing.")
        except Exception as e:
            st.error(f"Error: {e}")
            
    else:
        st.subheader("🏆 Accuracy Comparison")
        accuracies = {model: m['accuracy'] for model, m in metrics_table.items()}
        # Sort for better visual
        sorted_acc = dict(sorted(accuracies.items(), key=lambda item: item[1]))
        
        fig_comp = px.bar(
            x=list(sorted_acc.values()),
            y=list(sorted_acc.keys()),
            orientation='h',
            text=[f"{v:.1%}" for v in sorted_acc.values()],
            labels={'x': 'Accuracy', 'y': ''},
            color=list(sorted_acc.values()),
            color_continuous_scale="Teal",
            height=300
        )
        fig_comp.update_layout(
            margin=dict(l=0, r=0, t=20, b=0),
            template="plotly_white",
            font=dict(color="#2c3e50", family="Roboto"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(range=[0, 1.05], showgrid=False), # No grid needed with text labels
            yaxis=dict(showgrid=False),
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig_comp, use_container_width=True, theme=None)

