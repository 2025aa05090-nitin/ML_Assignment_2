"""
ML Assignment 2 - Obesity Risk Classification
Train all 6 classification models on Obesity Risk Classification dataset
"""

import json
import pickle
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    matthews_corrcoef,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier

try:
    from xgboost import XGBClassifier
    HAS_XGBOOST = True
except Exception:
    HAS_XGBOOST = False

# Dataset paths
DATA_DIR = Path("data")
MODEL_DIR = Path("model")
MODEL_DIR.mkdir(exist_ok=True)

# Try common obesity dataset file names
OBESITY_DATA_FILES = [
    "obesity_risk.csv",
    "ObesityDataSet.csv",
    "obesity.csv",
    "Obesity_Risk_Classification.csv",
]


def find_obesity_dataset():
    """Find the obesity dataset CSV file."""
    for filename in OBESITY_DATA_FILES:
        filepath = DATA_DIR / filename
        if filepath.exists():
            return filepath
    
    # Try to find any CSV in data directory
    csv_files = list(DATA_DIR.glob("*.csv"))
    if csv_files:
        return csv_files[0]
    
    raise FileNotFoundError(
        f"Obesity dataset not found. Please download and place in {DATA_DIR}/ folder.\n"
        f"Expected filenames: {OBESITY_DATA_FILES}"
    )


def load_obesity_dataset(path: Path) -> tuple[pd.DataFrame, str]:
    """
    Load obesity dataset, fix BMI inconsistencies, and identifying target.
    Returns: (dataframe, target_column_name)
    """
    df = pd.read_csv(path)
    
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # --- FIX DATA INCONSISTENCIES ---
    print("\n[INFO] Fixing data inconsistencies (Recalculating BMI & Targets)...")
    
    # 1. Ensure Height is in Meters for BMI calculation
    # If mean height > 10, assume it's cm
    if df['Height'].mean() > 10:
        df['Height_m'] = df['Height'] / 100
    else:
        df['Height_m'] = df['Height']

    # 2. Recalculate BMI (Weight / Height^2)
    # Use the calculated BMI as the source of truth
    df['BMI_Calculated'] = df['Weight'] / (df['Height_m'] ** 2)
    
    # 3. Regenerate Target based on Standard BMI Categories (Paleo et al.)
    # Underweight < 18.5
    # Normal 18.5 - 24.9
    # Overweight I 25.0 - 26.9
    # Overweight II 27.0 - 29.9
    # Obesity I 30.0 - 34.9
    # Obesity II 35.0 - 39.9
    # Obesity III >= 40.0
    
    def classify_bmi(bmi):
        if bmi < 18.5:
            return 'Insufficient_Weight'
        elif 18.5 <= bmi < 25.0:
            return 'Normal_Weight'
        elif 25.0 <= bmi < 27.0:
            return 'Overweight_Level_I'
        elif 27.0 <= bmi < 30.0:
            return 'Overweight_Level_II'
        elif 30.0 <= bmi < 35.0:
            return 'Obesity_Type_I'
        elif 35.0 <= bmi < 40.0:
            return 'Obesity_Type_II'
        else:
            return 'Obesity_Type_III'

    target_col = "NObeyesdad"
    # Overwrite target with consistent values
    df[target_col] = df['BMI_Calculated'].apply(classify_bmi)
    
    # 4. Update the 'BMI' feature to match reality (so models learn from correct BMI)
    # Check if 'BMI' column exists, otherwise create it
    if 'BMI' in df.columns:
        df['BMI'] = df['BMI_Calculated']
    else:
        df['BMI'] = df['BMI_Calculated']
        
    # Drop temporary columns
    df.drop(columns=['Height_m', 'BMI_Calculated'], inplace=True)
    
    print(f"[SUCCESS] Data fixed. Targets regenerated based on Height/Weight.")
    
    # --- END FIX ---

    # Handle missing values
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if col != target_col:
            df[col].fillna(df[col].median(), inplace=True)
    
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if col != target_col:
            df[col].fillna(df[col].mode()[0] if len(df[col].mode()) > 0 else 'Unknown', inplace=True)
    
    return df, target_col


def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    """Build preprocessing pipeline for mixed data types."""
    categorical_cols = X.select_dtypes(include=["object"]).columns.tolist()
    numeric_cols = [c for c in X.columns if c not in categorical_cols]

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=True)),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_cols),
            ("cat", categorical_transformer, categorical_cols),
        ],
        remainder="drop"
    )
    return preprocessor


def evaluate_model(name, model, X_test, y_test):
    """Evaluate model and return metrics."""
    y_pred = model.predict(X_test)
    
    # Get probabilities for AUC
    if hasattr(model, "predict_proba"):
        y_prob = model.predict_proba(X_test)
        # Handle multi-class: use probabilities for positive class
        if y_prob.shape[1] > 2:
            # Multi-class: use macro average or one-vs-rest
            y_prob_binary = y_prob[:, 1] if y_prob.shape[1] == 2 else y_prob.max(axis=1)
        else:
            y_prob_binary = y_prob[:, 1]
    elif hasattr(model, "decision_function"):
        scores = model.decision_function(X_test)
        y_prob_binary = (scores - scores.min()) / (scores.max() - scores.min() + 1e-9)
    else:
        y_prob_binary = None

    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred, average='weighted', zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, average='weighted', zero_division=0)),
        "f1": float(f1_score(y_test, y_pred, average='weighted', zero_division=0)),
        "mcc": float(matthews_corrcoef(y_test, y_pred)),
    }
    
    # Calculate AUC (handle multi-class)
    if y_prob_binary is not None:
        try:
            if len(np.unique(y_test)) == 2:
                # Binary classification
                metrics["auc"] = float(roc_auc_score(y_test, y_prob_binary))
            else:
                # Multi-class: use one-vs-rest
                metrics["auc"] = float(roc_auc_score(y_test, y_prob, multi_class='ovr', average='weighted'))
        except Exception as e:
            print(f"Warning: Could not calculate AUC for {name}: {e}")
            metrics["auc"] = float("nan")
    else:
        metrics["auc"] = float("nan")

    report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    cm = confusion_matrix(y_test, y_pred).tolist()

    return metrics, report, cm


def main():
    """Main training function."""
    print("=" * 60)
    print("ML Assignment 2 - Obesity Risk Classification")
    print("=" * 60)
    print()
    
    # Load dataset
    data_path = find_obesity_dataset()
    print(f"Loading dataset from: {data_path}")
    df, target_col = load_obesity_dataset(data_path)
    
    # Prepare features and target
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # Encode target if it's categorical
    if y.dtype == 'object':
        le = LabelEncoder()
        y = le.fit_transform(y)
        print(f"Target encoded. Classes: {np.unique(y)}")
        # Save label encoder for later use
        joblib.dump(le, MODEL_DIR / "label_encoder.pkl")
    
    print(f"\nFeatures: {X.shape[1]}")
    print(f"Instances: {X.shape[0]}")
    print(f"Target classes: {len(np.unique(y))}")
    print()
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    print()
    
    # Build preprocessor
    preprocessor = build_preprocessor(X)
    
    # Define models
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Decision Tree": DecisionTreeClassifier(random_state=42, max_depth=10),
        "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=7),
        "Naive Bayes": GaussianNB(),
        "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42, max_depth=10),
    }

    if HAS_XGBOOST:
        models["XGBoost"] = XGBClassifier(
            n_estimators=300,
            max_depth=5,
            learning_rate=0.1,
            subsample=0.9,
            colsample_bytree=0.9,
            eval_metric="logloss",
            random_state=42,
        )
    else:
        print("Warning: XGBoost not available. Install with: pip install xgboost")
    
    # Train and evaluate models
    metrics_table = {}
    reports = {}
    confusion_matrices = {}
    
    print("=" * 60)
    print("Training Models")
    print("=" * 60)
    print()
    
    for name, clf in models.items():
        print(f"Training {name}...")
        
        if name == "Naive Bayes":
            # GaussianNB does not accept sparse matrices
            preprocessor_nb = ColumnTransformer(
                transformers=preprocessor.transformers,
                remainder="drop",
                sparse_threshold=0.0,
            )
            pipeline = Pipeline(steps=[("preprocessor", preprocessor_nb), ("model", clf)])
        else:
            pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("model", clf)])

        pipeline.fit(X_train, y_train)
        metrics, report, cm = evaluate_model(name, pipeline, X_test, y_test)
        
        metrics_table[name] = metrics
        reports[name] = report
        confusion_matrices[name] = cm
        
        print(f"  Accuracy: {metrics['accuracy']:.4f}")
        print(f"  AUC: {metrics['auc']:.4f}")
        print(f"  F1: {metrics['f1']:.4f}")
        print()
        
        # Save model
        model_path = MODEL_DIR / f"{name.replace(' ', '_').lower()}.pkl"
        with open(model_path, 'wb') as f:
            pickle.dump(pipeline, f)
        print(f"  Model saved: {model_path}")
        print()
    
    # Save metrics
    with open(MODEL_DIR / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics_table, f, indent=2)

    with open(MODEL_DIR / "reports.json", "w", encoding="utf-8") as f:
        json.dump(reports, f, indent=2)

    with open(MODEL_DIR / "confusion_matrices.json", "w", encoding="utf-8") as f:
        json.dump(confusion_matrices, f, indent=2)
    
    print("=" * 60)
    print("Training Complete!")
    print("=" * 60)
    print(f"Models and metrics saved in {MODEL_DIR}/")
    print()
    print("Model Performance Summary:")
    print("-" * 60)
    for name, metrics in metrics_table.items():
        print(f"{name:25s} | Acc: {metrics['accuracy']:.4f} | AUC: {metrics['auc']:.4f} | F1: {metrics['f1']:.4f}")


if __name__ == "__main__":
    main()
