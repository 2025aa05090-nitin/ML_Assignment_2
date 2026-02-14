# ML Assignment 2

## Problem statement
Build and evaluate multiple classification models on a public dataset, then deploy a Streamlit app that allows model selection, metric display, and prediction on uploaded test data.

## Dataset description
Dataset: Obesity Risk Classification (Kaggle).

- **Source**: Kaggle - Obesity Risk Classification Dataset
- **Dataset Link**: https://www.kaggle.com/datasets/fernandoramirez/obesity-risk-classification
- **Rows after cleaning**: 600
- **Features**: 17 input features (numerical + categorical)
- **Target**: `NObeyesdad` (7 classes: Normal_Weight, Overweight_Level_I, Overweight_Level_II, Obesity_Type_I, Obesity_Type_II, Obesity_Type_III, Insufficient_Weight)
- **Source file**: `data/obesity_risk.csv`

## Models used
### Comparison Table

| ML Model Name | Accuracy | AUC | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 0.1833 | 0.5134 | 0.1566 | 0.1833 | 0.1672 | 0.0458 |
| Decision Tree | 0.1583 | 0.5024 | 0.1569 | 0.1583 | 0.1556 | 0.0162 |
| K-Nearest Neighbors | 0.1500 | 0.4785 | 0.1186 | 0.1500 | 0.1223 | 0.0026 |
| Naive Bayes | 0.1167 | 0.5022 | 0.1115 | 0.1167 | 0.1095 | -0.0289 |
| Random Forest | 0.1583 | 0.5325 | 0.1518 | 0.1583 | 0.1496 | 0.0145 |
| XGBoost | 0.1917 | 0.5282 | 0.1787 | 0.1917 | 0.1820 | 0.0548 |

### Observations

| ML Model Name | Observation about model performance |
|---|---|
| Logistic Regression | Best accuracy among all models (0.1833) with reasonable AUC (0.5134); performs relatively well as a baseline for multi-class classification on this dataset. |
| Decision Tree | Lower performance (0.1583 accuracy) with AUC near random (0.5024); likely struggles with the complexity of 7-class classification and may benefit from deeper trees or ensemble methods. |
| K-Nearest Neighbors | Lowest accuracy (0.1500) and AUC (0.4785); struggles with high-dimensional categorical features and the multi-class nature of the problem; sensitive to feature scaling. |
| Naive Bayes | Poorest performance (0.1167 accuracy) with negative MCC; the strong independence assumption is violated by correlated features in this health dataset, leading to poor classification. |
| Random Forest | Moderate performance (0.1583 accuracy) but highest AUC (0.5325); ensemble approach helps but still struggles with the 7-class classification task; may need more trees or different hyperparameters. |
| XGBoost | Second-best accuracy (0.1917) with good AUC (0.5282); gradient boosting helps capture complex patterns, making it competitive with Logistic Regression for this multi-class problem. |
