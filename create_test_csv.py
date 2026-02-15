from train_models_obesity import load_obesity_dataset, find_obesity_dataset
import pandas as pd

# Load the fixed dataset
data_path = find_obesity_dataset()
print(f"Loading data from {data_path}...")
df, target_col = load_obesity_dataset(data_path)

# Sample one instance from each class
print("Sampling 1 example per class for testing...")
test_df = df.groupby(target_col).apply(lambda x: x.sample(1, random_state=42)).reset_index(drop=True)

# Save to CSV
output_path = "test.csv"
test_df.to_csv(output_path, index=False)

print(f"Success! Created {output_path} with {len(test_df)} rows.")
print(test_df[[target_col, 'Height', 'Weight', 'BMI']].head(7))
