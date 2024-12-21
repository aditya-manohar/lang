import pandas as pd

def load_data(filename):
    if filename.endswith('.csv'):
        return pd.read_csv(filename)
    elif filename.endswith('.xlsx'):
        return pd.read_excel(filename)
    elif filename.endswith('.json'):
        return pd.read_json(filename)
    else:
        raise ValueError(f"Unsupported file type: {filename}")
