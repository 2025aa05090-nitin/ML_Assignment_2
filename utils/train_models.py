"""
ML Assignment 2 - Obesity Risk Classification
Train all 6 classification models on Obesity Risk Classification dataset
"""

import json
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
        f"Expected filenames: {OBESITY_DATA_FILES}\n"
        f"Download from: https://www.kaggle.com/datasets/fernandoramirez/obesity-risk-classification"
    )


def load_dataset(path: Path) -> tuple[pd.DataFrame, str]:
    """
    Load obesity dataset and identify target column.
    Returns: (dataframe, target_column_name)
    """
    df = pd.read_csv(path)
    
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"Columns: {list(df.columns)}")
    
    # Identify target column (common names for obesity risk classification)
    target_candidates = [
        col for col in df.columns 
        if any(word in col.lower() for word in [
            'obesity', 'risk', 'class', 'category', 'target', 
            'label', 'obesitylevel', 'no_obesity', 'obesity_type'
        ])
    ]
    
    if target_candidates:
        target_col = target_candidates[0]
        print(f"Target column identified: {target_col}")
    else:
        # Assume last column is target
        target_col = df.columns[-1]
        print(f"Using last column as target: {target_col}")
    
    # Handle missing values
    print(f"\nMissing values before cleaning:")
    print(df.isnull().sum().sum(), "total missing values")
    
    # For numeric columns, fill with median
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if col != target_col:
            df.loc[:, col] = df[col].fillna(df[col].median())
    
    # For categorical columns, fill with mode
    categorical_cols = df.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if col != target_col:
            mode_value = df[col].mode()[0] if len(df[col].mode()) > 0 else 'Unknown'
            df.loc[:, col] = df[col].fillna(mode_value)
    
    # Drop rows with missing target
    df = df.dropna(subset=[target_col])
    
    print(f"Dataset after cleaning: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # Check if we have enough features (minimum 12 required)
    feature_count = df.shape[1] - 1  # Excluding target
    if feature_count < 12:
        print(f"WARNING: Only {feature_count} features found. Assignment requires minimum 12 features.")
    
    # Check if we have enough instances (minimum 500 required)
    if df.shape[0] < 500:
        print(f"WARNING: Only {df.shape[0]} instances found. Assignment requires minimum 500 instances.")
    
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
    df, target_col = load_dataset(data_path)
    
    # Prepare features and target
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # Encode target if it's categorical
    le = None
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
        joblib.dump(pipeline, model_path)
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
