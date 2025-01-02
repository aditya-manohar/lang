import re
import pandas as pd
import statistics

def clean_data(data, strategy="mean", custom_value=None, columns=None):
    try:
        if strategy == "remove duplicates":
            before = len(data)
            data.drop_duplicates(inplace=True)
            after = len(data)
            print(f"Removed {before - after} duplicate rows.")

        elif strategy in ["mean", "median", "mode"]:
            if columns is None: 
                columns = data.columns
            
            for column in columns:
                if data[column].isnull().any():
                    if custom_value is not None:  
                        custom_value = float(custom_value) 
                        data[column].fillna(custom_value, inplace=True)
                    else:  
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
        # Handle multiple columns as a string (split by commas)
        if isinstance(columns, str):
            columns = [col.strip() for col in columns.split(',')]  # Split and clean up column names

        # Ensure that columns to remove are actually in the data
        missing_columns = [col for col in columns if col not in data.columns]
        if missing_columns:
            print(f"Warning: The following columns were not found: {', '.join(missing_columns)}")

        # Drop the columns that are present in the DataFrame and return modified data
        data = data.drop(columns=[col for col in columns if col in data.columns], inplace=False)
        print(f"Columns {', '.join(columns)} removed successfully.")
    
    except Exception as e:
        print(f"Error removing column(s) '{columns}': {e}")

    return data  # Return modified data for chaining or non-chaining

def mean(var_name, variables):
    if var_name in variables:
        data = variables[var_name]
        return statistics.mean(data)
    else:
        raise ValueError(f"Variable {var_name} not found.")

def median(var_name, variables):
    if var_name in variables:
        data = variables[var_name]
        return statistics.median(data)
    else:
        raise ValueError(f"Variable {var_name} not found.")

def mode(var_name, variables):
    if var_name in variables:
        data = variables[var_name]
        try:
            return statistics.mode(data)
        except statistics.StatisticsError:
            raise ValueError(f"No unique mode found for {var_name}.")
    else:
        raise ValueError(f"Variable {var_name} not found.")

def fill_missing_values(data, strategy, columns=None, custom_value=None):
    try:
        if columns is None:  # If no specific columns are mentioned, apply to all
            columns = data.columns
        
        for column in columns:
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
                        mode_value = data[column].mode()[0] if not data[column].mode().empty else None
                        data[column].fillna(mode_value, inplace=True)
            print(f"Filled missing values in column: {column} using {strategy}")
    except Exception as e:
        print(f"Error in fill_missing_values: {e}")
    return data

def remove_rows_with_null(data):
    try:
        before = len(data)
        data = data.dropna()  # Drop rows with any null values
        after = len(data)
        print(f"Removed {before - after} rows with null values.")
    except Exception as e:
        print(f"Error removing rows with null values: {e}")
    return data

def rename_column(data, old_name, new_name):
    """Renames a column in the dataset."""
    if old_name in data.columns:
        data.rename(columns={old_name: new_name}, inplace=True)
    else:
        raise KeyError(f"Column '{old_name}' not found.")
    return data



