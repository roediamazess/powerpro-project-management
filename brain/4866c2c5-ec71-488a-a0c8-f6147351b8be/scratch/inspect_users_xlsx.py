import pandas as pd
import os

file_path = r'c:\Website\powerpro-project-management\assets\users.xlsx'

if os.path.exists(file_path):
    try:
        df = pd.read_excel(file_path)
        print("Columns in Excel:")
        print(df.columns.tolist())
        print("\nFirst 3 rows:")
        print(df.head(3).to_string())
    except Exception as e:
        print(f"Error reading Excel: {e}")
else:
    print(f"File not found: {file_path}")
