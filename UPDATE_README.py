"""
Script to automatically update README.md with metrics from training results.
Run this after training models to populate the README with actual metrics.
"""

import json
from pathlib import Path

MODEL_DIR = Path("model")
README_PATH = Path("README.md")

def update_readme_with_metrics():
    """Update README.md with actual metrics from training."""
    
    # Load metrics
    metrics_path = MODEL_DIR / "metrics.json"
    if not metrics_path.exists():
        print("Error: metrics.json not found. Run train_models.py first.")
        return
    
    with open(metrics_path, "r") as f:
        metrics = json.load(f)
    
    # Read current README
    if not README_PATH.exists():
        print("Error: README.md not found.")
        return
    
    with open(README_PATH, "r") as f:
        readme_content = f.read()
    
    # Generate comparison table
    table_rows = []
    for model_name in ["Logistic Regression", "Decision Tree", "K-Nearest Neighbors", 
                       "Naive Bayes", "Random Forest", "XGBoost"]:
        if model_name in metrics:
            m = metrics[model_name]
            table_rows.append(
                f"| {model_name} | {m['accuracy']:.4f} | {m['auc']:.4f} | "
                f"{m['precision']:.4f} | {m['recall']:.4f} | {m['f1']:.4f} | {m['mcc']:.4f} |"
            )
        else:
            table_rows.append(
                f"| {model_name} | N/A | N/A | N/A | N/A | N/A | N/A |"
            )
    
    # Replace comparison table
    import re
    table_pattern = r'\| ML Model Name.*?\| XGBoost.*?\|'
    new_table = "| ML Model Name | Accuracy | AUC | Precision | Recall | F1 | MCC |\n"
    new_table += "|---|---:|---:|---:|---:|---:|---:|\n"
    new_table += "\n".join(table_rows)
    
    readme_content = re.sub(table_pattern, new_table, readme_content, flags=re.DOTALL)
    
    # Save updated README
    with open(README_PATH, "w") as f:
        f.write(readme_content)
    
    print("README.md updated with metrics!")
    print("\nNote: You still need to manually update the 'Observations' section")
    print("      and the 'Dataset description' section with actual numbers.")

if __name__ == "__main__":
    update_readme_with_metrics()
