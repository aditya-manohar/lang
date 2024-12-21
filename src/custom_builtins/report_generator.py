def generate_report(data, cleaning_summary):
    """
    Generate a report summarizing the cleaning steps and the state of the data.

    Args:
        data (pd.DataFrame): The cleaned dataset.
        cleaning_summary (dict): Information about cleaning steps applied.

    Returns:
        str: Formatted report.
    """
    report = []
    report.append("===== Data Cleaning Report =====")
    report.append(f"Rows: {data.shape[0]} | Columns: {data.shape[1]}")
    report.append("\n--- Cleaning Summary ---")
    
    # Loop through the cleaning summary dictionary and add steps to the report
    for step, details in cleaning_summary.items():
        report.append(f"{step}: {details}")
    
    report.append("\n--- Data Preview ---")
    # Preview first rows of the data (first 5 rows)
    report.append(data.head().to_string(index=False))  # Preview first rows without the index
    
    return "\n".join(report)  # Return the formatted report as a string
