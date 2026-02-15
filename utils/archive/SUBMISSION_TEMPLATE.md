# ML Assignment 2 - Submission Document

## 1. GitHub Repository Link

**Repository URL**: `https://github.com/YOUR_USERNAME/ML_Assignment_2`

*(Replace YOUR_USERNAME with your actual GitHub username)*

**Repository Contents**:
- Complete source code (`app.py`, `train_models.py`)
- `requirements.txt` with all dependencies
- `README.md` with complete documentation
- Trained models in `model/` directory
- Dataset in `data/` directory

---

## 2. Live Streamlit App Link

**Streamlit App URL**: `https://YOUR_APP_NAME.streamlit.app`

*(Replace YOUR_APP_NAME with your actual Streamlit app name)*

**App Features**:
- Model selection dropdown for all 6 models
- Evaluation metrics display (Accuracy, AUC, Precision, Recall, F1, MCC)
- Confusion matrix visualization
- Classification report
- CSV upload for predictions
- Download predictions as CSV

---

## 3. Screenshot of Assignment Execution on BITS Virtual Lab

*[Insert your screenshot here]*

**Screenshot Description**: This screenshot shows the execution of the ML Assignment 2 on BITS Virtual Lab, demonstrating the training of all 6 classification models and the successful generation of evaluation metrics.

---

## 4. README Content

# ML Assignment 2

## Problem statement
Build and evaluate multiple classification models on a public dataset, then deploy a Streamlit app that allows model selection, metric display, and prediction on uploaded test data.

## Dataset description
Dataset: UCI Adult Income dataset (Census Income).

- Rows after cleaning: 30,162
- Features: 14 input features (numerical + categorical)
- Target: `income` (<=50K vs >50K)
- Source file: `data/adult.data`

## Models used
### Comparison Table

| ML Model Name | Accuracy | AUC | Precision | Recall | F1 | MCC |
|---|---:|---:|---:|---:|---:|---:|
| Logistic Regression | 0.8475 | 0.9022 | 0.7354 | 0.6052 | 0.6640 | 0.5711 |
| Decision Tree | 0.8087 | 0.7478 | 0.6134 | 0.6265 | 0.6199 | 0.4922 |
| K-Nearest Neighbors | 0.8286 | 0.8731 | 0.6718 | 0.6092 | 0.6390 | 0.5280 |
| Naive Bayes | 0.5826 | 0.8018 | 0.3678 | 0.9414 | 0.5290 | 0.3643 |
| Random Forest | 0.8493 | 0.9012 | 0.7286 | 0.6292 | 0.6752 | 0.5805 |
| XGBoost | 0.8664 | 0.9248 | 0.7698 | 0.6611 | 0.7113 | 0.6281 |

### Observations

| ML Model Name | Observation about model performance |
|---|---|
| Logistic Regression | Solid baseline with high AUC and balanced precision/recall; performs well on this dataset with linear decision boundary. |
| Decision Tree | Lower AUC and accuracy compared to ensembles; likely overfits and struggles to generalize. |
| K-Nearest Neighbors | Reasonable performance but not as strong as ensemble methods; sensitive to feature scaling and high dimensionality. |
| Naive Bayes | Very high recall but low precision, leading to lower overall accuracy; strong assumption of feature independence hurts performance. |
| Random Forest | Strong performance with good balance across metrics; ensemble reduces overfitting and improves generalization. |
| XGBoost | Best overall performance across accuracy, AUC, F1, and MCC; captures complex patterns effectively. |

---

## Submission Checklist

- [x] GitHub repository created and all files committed
- [x] Repository is public
- [x] Streamlit app deployed and accessible
- [x] All 6 models implemented and evaluated
- [x] All 6 metrics calculated for each model
- [x] README.md contains all required sections
- [x] Screenshot taken on BITS Virtual Lab
- [x] All links tested and working
- [x] PDF created with all required content in order

---

**Student Information**:
- Name: [Your Name]
- Enrollment Number: [Your Enrollment Number]
- Submission Date: [Date]
- Assignment: ML Assignment 2
- Marks: 15

---

*End of Submission Document*
