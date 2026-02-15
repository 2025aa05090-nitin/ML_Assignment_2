import json
import pickle
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import accuracy_score, f1_score

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
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
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

    /* Sidebar - Distinct */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #ddd;
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
DATA_DIR = Path("data")

# --- Load Utilities ---
metrics_path = MODEL_DIR / "metrics.json"
reports_path = MODEL_DIR / "reports.json"
confusion_path = MODEL_DIR / "confusion_matrices.json"
label_encoder_path = MODEL_DIR / "label_encoder.pkl"

if not metrics_path.exists():
    st.error("Models not found. Run `train_models.py` first.")
    st.stop()

with open(metrics_path, "r", encoding="utf-8") as f:
    metrics_table = json.load(f)

with open(reports_path, "r", encoding="utf-8") as f:
    reports_table = json.load(f)

with open(confusion_path, "r", encoding="utf-8") as f:
    confusion_matrices = json.load(f)

model_names = list(metrics_table.keys())

# --- HELPER FUNCTIONS ---
@st.cache_data
def load_data():
    # Attempt to load original dataset for EDA
    possible_paths = [DATA_DIR/"obesity_risk.csv", Path("obesity_risk.csv"), Path("data/obesity_risk.csv")]
    for p in possible_paths:
        if p.exists():
            return pd.read_csv(p)
    return None

@st.cache_resource
def load_all_models():
    models = {}
    for name in model_names:
        path = MODEL_DIR / f"{name.replace(' ', '_').lower()}.pkl"
        if path.exists():
            with open(path, "rb") as f:
                models[name] = pickle.load(f)
    return models

# --- SIDEBAR ---
with st.sidebar:
    st.title("🎛️ Control Panel")

    st.markdown("### 1. Model Selection")
    selected_model = st.selectbox("Choose Model", model_names)

    st.markdown("---")
    st.markdown("### 2. Download Test Data")
    st.markdown("Get standard test data to try predictions:")
    
    # Check if test.csv exists locally for download
    test_csv_path = Path("test.csv")
    if test_csv_path.exists():
        with open(test_csv_path, "rb") as f:
            st.download_button(
                label="📄 Download test.csv",
                data=f,
                file_name="test.csv",
                mime="text/csv"
            )
    else:
        st.warning("test.csv not found locally.")

    st.markdown(
        "[🔗 View on GitHub](https://github.com/2025aa05090-nitin/ML_Assignment_2/blob/main/test.csv)", 
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    st.info("💡 **Tip:** Go to the 'Live Predictions' tab to upload file!")


# --- MAIN LAYOUT ---
st.markdown("<h1>🥑 Obesity Risk Predictor 🚀</h1>", unsafe_allow_html=True)

# Define Tabs - "Model Evaluation" is FIRST as requested
tab1, tab2, tab3, tab4 = st.tabs(["📝 Model Evaluation", "📊 EDA & Insights", "🏆 Comparison", "🔮 Live Predictions"])

# --- TAB 1: MODEL EVALUATION (Grading Requirement) ---
with tab1:
    st.header(f"Performance: {selected_model}")
    
    # 1. Metrics Row
    metrics = metrics_table[selected_model]
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Accuracy", f"{metrics['accuracy']:.1%}")
    m2.metric("AUC Score", f"{metrics['auc']:.3f}")
    m3.metric("F1 Score", f"{metrics['f1']:.3f}")
    m4.metric("MCC Score", f"{metrics['mcc']:.3f}")
    
    st.markdown("---")
    
    # 2. Confusion Matrix & Classification Report
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.subheader("Confusion Matrix")
        cm = np.array(confusion_matrices[selected_model])
        
        # Load labels
        class_names = [f"C{i}" for i in range(cm.shape[0])]
        if label_encoder_path.exists():
            try:
                le = joblib.load(label_encoder_path)
                class_names = [name[:10]+".." if len(name)>10 else name for name in le.classes_.tolist()]
            except:
                pass

        fig_cm = px.imshow(
            cm,
            text_auto=True,
            labels=dict(x="Predicted", y="True", color="Count"),
            x=class_names,
            y=class_names,
            color_continuous_scale="Blues",
            aspect="auto",
            height=400,
        )
        fig_cm.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_cm, use_container_width=True)

    with c2:
        st.subheader("Classification Report")
        if selected_model in reports_table:
            # Convert JSON report to DataFrame
            report_data = reports_table[selected_model]
            # Convert to DF
            df_rep = pd.DataFrame(report_data).transpose()
            # Filter support column if needed, or keep all
            st.dataframe(df_rep.style.format("{:.3f}").background_gradient(cmap="Greens", subset=["f1-score", "precision", "recall"]), height=400, use_container_width=True)
        else:
            st.info("Detailed classification report not available.")

# --- TAB 2: EDA ---
with tab2:
    st.header("Exploratory Data Analysis")
    df = load_data()
    
    if df is not None:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Target Distribution")
            target_col = df.columns[-1] 
            fig_target = px.histogram(df, x=target_col, color=target_col, title="Class Imbalance Check")
            fig_target.update_layout(showlegend=False, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_target, use_container_width=True)
            
        with c2:
            st.subheader("Weight vs Height")
            if 'Weight' in df.columns and 'Height' in df.columns:
                fig_scatter = px.scatter(df, x="Height", y="Weight", color=target_col, title="Body Mass Clusters")
                fig_scatter.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_scatter, use_container_width=True)
        
        st.subheader("Correlation Heatmap (Numerical)")
        numeric_df = df.select_dtypes(include=[np.number])
        if not numeric_df.empty:
            corr = numeric_df.corr()
            fig_corr = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale="RdBu_r")
            fig_corr.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.warning("Original training data not found for EDA.")

# --- TAB 3: MODEL COMPARISON ---
with tab3:
    st.header("Model Leaderboard")
    
    accuracies = {model: m['accuracy'] for model, m in metrics_table.items()}
    sorted_acc = dict(sorted(accuracies.items(), key=lambda item: item[1]))
    
    fig_comp = px.bar(
        x=list(sorted_acc.values()),
        y=list(sorted_acc.keys()),
        orientation='h',
        text=[f"{v:.1%}" for v in sorted_acc.values()],
        labels={'x': 'Accuracy', 'y': ''},
        color=list(sorted_acc.values()),
        color_continuous_scale="Teal",
        title="Accuracy Leaderboard"
    )
    fig_comp.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(range=[0, 1.05], showgrid=False),
        yaxis=dict(showgrid=False),
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_comp, use_container_width=True)

    st.subheader("Detailed Metrics Table")
    metrics_df = pd.DataFrame(metrics_table).T
    st.dataframe(metrics_df.style.format("{:.4f}").background_gradient(cmap="Blues"), use_container_width=True)

# --- TAB 4: LIVE PREDICTIONS ---
with tab4:
    st.header("Multi-Model Prediction Lab 🧪")
    
    uploaded_file = st.file_uploader("📂 Upload CSV File (e.g., test.csv)", type=["csv"])
    
    if uploaded_file is not None:
        try:
            input_df = pd.read_csv(uploaded_file)
            st.success(f"Loaded {len(input_df)} rows successfully!")
            
            # Identify Target Column (if exists) for validation
            possible_targets = ['NObeyesdad', 'Obesity_Level', 'Target', 'Label']
            target_col = next((col for col in input_df.columns if col in possible_targets), None)
            
            X_input = input_df.copy()
            y_true = None
            
            if target_col:
                st.info(f"✅ Ground Truth found: `{target_col}`. Calculating metrics...")
                y_true = X_input.pop(target_col)
            
            # Load Label Encoder
            le = None
            if label_encoder_path.exists():
                le = joblib.load(label_encoder_path)

            # Load Models
            models = load_all_models()
            
            results = {} # Store preds
            model_metrics = [] # Store accuracy/f1 if target exists
            
            # Run All Models
            for name, model in models.items():
                preds = model.predict(X_input)
                
                # Inverse transform if LE exists
                if le:
                    try:
                        preds_decoded = le.inverse_transform(preds)
                    except:
                        preds_decoded = preds
                else:
                    preds_decoded = preds
                
                # Store
                res_df = input_df.copy()
                res_df["Predicted_Class"] = preds_decoded
                results[name] = res_df
                
                # Calculate Metrics
                if y_true is not None:
                    acc = accuracy_score(y_true, preds_decoded)
                    f1 = f1_score(y_true, preds_decoded, average="weighted")
                    model_metrics.append({"Model": name, "Test Accuracy": acc, "Test F1": f1})

            # display Comparison Table (if metrics)
            if model_metrics:
                st.subheader("🏆 Performance on Uploaded Data")
                perf_df = pd.DataFrame(model_metrics).set_index("Model").sort_values("Test Accuracy", ascending=False)
                st.dataframe(perf_df.style.format("{:.2%}"), use_container_width=True)
                
                fig_perf = px.bar(
                    perf_df, x="Test Accuracy", y=perf_df.index, orientation='h',
                    text_auto=".1%", title="Accuracy on NEW Data", color="Test Accuracy", color_continuous_scale="Purples"
                )
                fig_perf.update_layout(xaxis_range=[0, 1.05])
                st.plotly_chart(fig_perf, use_container_width=True)

            # Tab-wise Predictions
            st.subheader("📑 Detailed Predictions by Model")
            model_tabs = st.tabs(list(results.keys()))
            
            for tab, (name, res_df) in zip(model_tabs, results.items()):
                with tab:
                    st.write(f"**Predictions using {name}**")
                    st.dataframe(res_df, use_container_width=True)
                    csv = res_df.to_csv(index=False)
                    st.download_button(f"📥 Download {name} Results", csv, f"{name}_predictions.csv", "text/csv")
                    
        except Exception as e:
            st.error(f"Error processing file: {e}")

    else:
        st.info("👆 Upload a CSV file to see predictions from all models simultaneously.")
