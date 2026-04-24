import pandas as pd
import os

file_path = '/app/assets/projects.xlsx'
if not os.path.exists(file_path):
    # Try another common path if the above fails
    file_path = '/app/projects.xlsx'

try:
    df = pd.read_excel(file_path)
    print("COLUMNS:")
    print(df.columns.tolist())
    print("\nSAMPLE DATA (1 row):")
    print(df.head(1).to_dict(orient='records'))
except Exception as e:
    print(f"ERROR: {e}")
