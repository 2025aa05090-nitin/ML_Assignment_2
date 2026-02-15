# ML Assignment 2

## Problem statement
Build and evaluate multiple classification models on a public dataset, then deploy a Streamlit app that allows model selection, metric display, and prediction on uploaded test data.

## Dataset description
Dataset: Obesity Risk Classification (Kaggle).

- **Source**: Kaggle - Obesity Risk Classification Dataset
- **Dataset Link**: https://www.kaggle.com/datasets/fernandoramirez/obesity-risk-classification
- **Rows**: 600
- **Features**: 17 input features (numerical + categorical)
- **Target**: `NObeyesdad` (7 classes: Normal_Weight, Overweight_Level_I, Overweight_Level_II, Obesity_Type_I, Obesity_Type_II, Obesity_Type_III, Insufficient_Weight)
- **Source file**: `data/obesity_risk.csv`

## Models used
### Comparison Table

| ML Model Name | Accuracy | AUC | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 0.7417 | 0.9511 | 0.7250 | 0.7417 | 0.7123 | 0.6651 |
| Decision Tree | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| K-Nearest Neighbors | 0.5000 | 0.7986 | 0.4362 | 0.5000 | 0.4481 | 0.3347 |
| Naive Bayes | 0.8583 | 0.9853 | 0.8869 | 0.8583 | 0.8633 | 0.8213 |
| Random Forest | 0.9000 | 0.9965 | 0.8580 | 0.9000 | 0.8742 | 0.8738 |
| XGBoost | 0.9917 | 1.0000 | 0.9944 | 0.9917 | 0.9921 | 0.9894 |

### Observations

| ML Model Name | Observation about model performance |
|---|---|
| Logistic Regression | Decent baseline (74%) but struggles with non-linear relationships in biological data compared to tree-based models. |
| Decision Tree | **Perfect Performance (100%)**. The model mastered the deterministic rules (BMI = Weight/Height²) underlying the dataset labels. |
| K-Nearest Neighbors | Weakest performer (50%). Likely impacted by the high dimensionality (after encoding) and scale differences, despite feature scaling. |
| Naive Bayes | Surprisingly strong (86%), though the independence assumption is theoretically violated by correlated features like Weight and BMI. |
| Random Forest | Strong performance (90%) but slightly overfitted compared to the single Decision Tree, possibly due to noise in the bagging process or hyperparameter settings. |
| XGBoost | **Excellent (99.2%)**. Nearly perfect. It captures complex patterns effectively and is the most robust alternative to the Decision Tree. |

## Deployment
The application is deployed on Streamlit Cloud.
- **App URL**: [Link to Streamlit App](https://mlassignment2-2025aa05090.streamlit.app/)
- **Features**:
    - **EDA Tab**: Visualizes target distribution and correlations.
    - **Model Comparison**: Interactive leaderboards.
    - **Live Predictions**: Upload CSV to run all 6 models simultaneously.
