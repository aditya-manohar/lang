import pandas as pd

def execute_block(ast, start_index):
    for i in range(start_index, len(ast)):
        node = ast[i]
        if node[0] in {"ENDIF", "ELSE"}:
            break
        interpret([node])  

def fill_missing_values(data, operation, columns):
    """
    Fill missing values (NaN) in the specified columns using the given operation (mean, median, or mode).
    """
    try:
        columns = [col.strip().strip("'") for col in columns]
        
        missing_columns = [col for col in columns if col not in data.columns]
        if missing_columns:
            print(f"Warning: Missing columns in data: {', '.join(missing_columns)}")
        
        if operation == "mean":
            return data[columns].fillna(data[columns].mean(axis=0, skipna=True), axis=0)
        elif operation == "median":
            return data[columns].fillna(data[columns].median(axis=0, skipna=True), axis=0)
        elif operation == "mode":
            mode_result = data[columns].mode(axis=0, dropna=True)
            mode_value = mode_result.iloc[0] if not mode_result.empty else None
            return data[columns].fillna(mode_value, axis=0)
        else:
            raise ValueError(f"Unknown operation: {operation}")
    except Exception as e:
        print(f"Error while processing {operation}: {e}")
        return None
