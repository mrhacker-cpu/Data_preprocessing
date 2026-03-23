import pandas as pd

def load_file(file_path):
    try:
        if file_path.endswith(".csv"):
            return pd.read_csv(file_path)

        elif file_path.endswith(".xlsx"):
            return pd.read_excel(file_path, engine="openpyxl")

        else:
            print("Unsupported file format")
            return None

    except Exception as e:
        print("Error loading file:", e)
        return None