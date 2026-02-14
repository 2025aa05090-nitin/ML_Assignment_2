# ML Assignment 2

## Problem statement
Build and evaluate multiple classification models on a public dataset, then deploy a Streamlit app that allows model selection, metric display, and prediction on uploaded test data.

## Dataset description
Dataset: Obesity Risk Classification (Kaggle)

- **Source**: Kaggle - Obesity Risk Classification Dataset
- **Dataset Link**: https://www.kaggle.com/datasets/fernandoramirez/obesity-risk-classification
- **Rows**: [Will be updated after training - minimum 500 required]
- **Features**: [Will be updated after training - minimum 12 required]
- **Target**: Obesity risk classification (multi-class or binary classification)
- **Source file**: `data/obesity_risk.csv` (or similar)

**Note**: After running `train_models.py`, update this section with actual numbers from the training output.

## Models used
### Comparison Table

| ML Model Name | Accuracy | AUC | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| Decision Tree | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| K-Nearest Neighbors | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| Naive Bayes | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| Random Forest | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |
| XGBoost | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] | [TBD] |

**Note**: After training, copy the metrics from `model/metrics.json` or from the training output to fill this table.

### Observations

| ML Model Name | Observation about model performance |
|---|---|
| Logistic Regression | [Update after training - analyze performance based on metrics] |
| Decision Tree | [Update after training - analyze performance based on metrics] |
| K-Nearest Neighbors | [Update after training - analyze performance based on metrics] |
| Naive Bayes | [Update after training - analyze performance based on metrics] |
| Random Forest | [Update after training - analyze performance based on metrics] |
| XGBoost | [Update after training - analyze performance based on metrics] |

**Note**: After training, analyze each model's performance and write observations based on:
- Accuracy and AUC scores
- Precision, Recall, and F1 balance
- Comparison with other models
- Strengths and weaknesses for this specific dataset

## Instructions

1. **Download the dataset** from Kaggle (see `DATASET_INSTRUCTIONS.md`)
2. **Place the CSV file** in the `data/` folder
3. **Run training**: `python3 train_models.py`
4. **Update this README** with actual metrics from training
5. **Run Streamlit app**: `streamlit run app.py`
