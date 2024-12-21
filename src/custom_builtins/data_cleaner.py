import re
import pandas as pd

def clean_data(data, strategy="mean", custom_value=None):
    try:
        if strategy == "remove duplicates":
            before = len(data)
            data.drop_duplicates(inplace=True)
            after = len(data)
            print(f"Removed {before - after} duplicate rows.")

        elif strategy in ["mean", "median", "mode"]:
            for column in data.columns:
                if data[column].isnull().any():
                    if custom_value is not None:  # Use custom value if provided
                        custom_value = float(custom_value)  # Ensure numeric value
                        data[column].fillna(custom_value, inplace=True)
                    else:  # Use default mean/median/mode
                        if strategy == "mean":
                            data[column].fillna(data[column].mean(), inplace=True)
                        elif strategy == "median":
                            data[column].fillna(data[column].median(), inplace=True)
                        elif strategy == "mode":
                            mode_value = data[column].mode()[0]
                            data[column].fillna(mode_value, inplace=True)
        else:
            raise ValueError(f"Unsupported cleaning strategy: {strategy}")
        
    except Exception as e:
        print(f"Error cleaning data: {e}")
    return data

def remove_rows(data, conditions):
    try:
        condition_list = conditions.split(',')
        for condition in condition_list:
            condition = condition.strip()  # Remove extra spaces
            print(f"Processing condition: {condition}")

            # Validate and process the condition
            match = re.match(r"(.+?)([<>=!]+)(.+)", condition)
            if not match:
                raise ValueError(f"Invalid condition syntax: {condition}")

            column, operator, value = match.groups()
            column, operator, value = column.strip(), operator.strip(), value.strip()

            # Ensure column exists
            if column not in data.columns:
                print(f"Error: Column '{column}' not found.")
                continue

            # Handle string values enclosed in single or double quotes
            if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
                value = value.strip("'").strip('"')  # Remove surrounding quotes
                value = repr(value)  # Add proper quotes for Pandas query

            # Convert to numeric if possible
            else:
                try:
                    value = float(value) if '.' in value else int(value)
                except ValueError:
                    value = repr(value)  # Treat as string if not numeric

            # Build the query string
            query = f"{column} {operator} {value}"
            print(f"Generated query: {query}")

            # Remove rows matching the condition
            before = len(data)
            data = data.query(f"not ({query})")  # Keep rows not matching the condition
            after = len(data)
            print(f"Rows removed: {before - after} based on condition: {condition}")

    except Exception as e:
        print(f"Error in remove_rows: {e}")
    return data


def remove_columns(data, columns):
    try:
        # Handle multiple columns
        if isinstance(columns, list):
            for col in columns:
                if col in data.columns:
                    data = data.drop(columns=[col], inplace=False)
                    print(f"Column {col} removed successfully")
                else:
                    print(f"Error: column '{col}' not found in the dataset")
        # Handle single column
        elif columns in data.columns:
            data = data.drop(columns=[columns], inplace=False)
            print(f"Column {columns} removed successfully")
        else:
            print(f"Error: column '{columns}' not found in the dataset")
    except Exception as e:
        print(f"Error removing columns '{columns}': {e}")
    return data