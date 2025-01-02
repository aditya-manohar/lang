from custom_builtins.data_loader import load_data
from custom_builtins.data_cleaner import clean_data,remove_rows,remove_columns,mean,median,mode,fill_missing_values,remove_rows_with_null,rename_column

variables = {}

def interpret(ast):
    for node in ast:
        if node[0] == "STRING":
            print(node[1]) 

        elif node[0] == "EXPRESSION":
            expression = node[1]
            try:
                if isinstance(expression, list):
                    result = []
                    for part in expression:
                        part = part.strip() 
                        if part.startswith('"') and part.endswith('"'): 
                            result.append(part[1:-1])  
                        elif part in variables:  
                            result.append(str(variables[part]))
                        else:
                            raise NameError(f"Variable or string {part} not recognized.")
                    print("".join(result)) 
                    continue

                if "+" in expression or "-" in expression or "*" in expression or "/" in expression or "%" in expression or "**" in expression:
                    for var in variables:
                        expression = expression.replace(var, str(variables[var])) 
                    result = eval(expression) 
                    print(result)
                    continue

                else:
                    if expression in variables:
                        print(variables[expression]) 
                    else:
                        print(expression)
            except Exception as e:
                print(f"Error evaluating expression: {e}")

        elif node[0] == "SET":
            var_name = node[1]
            var_type = node[2]
            value = node[3]
            if var_type == "STRING":
                variables[var_name] = value
            elif var_type == "NUMBER":
                variables[var_name] = value
            elif var_type == "BOOLEAN":
                variables[var_name] = value
            elif var_type == "FLOAT":
                variables[var_name] = value
            elif var_type == "LOAD":
                variables[var_name] = load_data(value)
            else:
                raise ValueError(f"Unsupported variable type {var_type}")
            
        elif node[0] == "DECLARE":
            var_name = node[1]
            if var_name not in variables:
                variables[var_name] = None
            else:
                print(f"{var_name} already declared")
            
        elif node[0] == "INPUT":
            var_name = node[1]
            user_input = input(f"Enter value for {var_name}: ")
            variables[var_name] = int(user_input)  # Assuming the input is an integer
            print(f"Input received: {var_name} = {variables[var_name]}")

        elif node[0] == "TYPE":
            var_name = node[1]
            if var_name in variables:
                print(type(variables[var_name]).__name__)  # Output the type of the variable
            else:
                print(f"Error: Variable {var_name} not found.")

        elif node[0] == "IF":
            condition = node[1]
            block = node[2]
            try:
                if eval(condition,{},variables):
                    interpret(block)
            except Exception as e:
                print(f"Error evaluating condition '{condition}' : {e}")

        elif node[0] == "ELSE":
            block = node[1]
            interpret(block)  

        elif node[0] == "LOAD":
            file_path = node[1]
            var_name = node[2]
            try:
                data = load_data(file_path)
                variables[var_name] = data  
                print(f"{file_path} stored in {var_name}")
            except Exception as e:
                print(f"Error loading file '{file_path}' : {e}")

        elif node[0] == "CLEAN":
            var_name = node[1]
            strategy = node[2]
            custom_value = node[3]

            if var_name in variables:
                data = variables[var_name]
                try:
                    if strategy == "remove duplicates":
                        variables[var_name] = clean_data(variables[var_name], strategy, custom_value)
                        print(f"cleaned using {strategy}")
                    elif strategy == "remove rows":
                        variables[var_name] = remove_rows(variables[var_name], custom_value)
                        print(f"cleaned using {strategy} where {custom_value}")
                    elif strategy == "remove columns":
                        if isinstance(custom_value, list): 
                            for col in custom_value:
                                variables[var_name] = remove_columns(variables[var_name], col) 
                                print(f"cleaned using {strategy} column {col}")
                        else:
                            variables[var_name] = remove_columns(variables[var_name], custom_value)
                            print(f"cleaned using {strategy} column {custom_value}")
                    else:
                        variables[var_name] = clean_data(variables[var_name], strategy, custom_value)
                except Exception as e:
                    print(f"Error cleaning data in '{var_name}' : {e}")
            else:
                print(f"Variable '{var_name}' not found")

        elif node[0] == "CHAIN":
            var_name = node[1]
            steps = node[2]
            current_data = variables[var_name]

            for step in steps:
                if step == "remove duplicates":
                    current_data = clean_data(current_data,"remove duplicates")
                elif step.startswith("remove rows where"):
                    condition = step.split("where")[-1].strip()
                    current_data = remove_rows(current_data, condition)
                elif step.startswith("remove columns"):
                    parts = step.split(" ")
                    if len(parts) == 3 and parts[0] == 'remove' and parts[1] == 'columns':
                        column_name = parts[2]
                        current_data= remove_columns(current_data,column_name)
                    else:
                        raise ValueError(f"Invalid chain operation : {step}")
                elif step.startswith("mean for"):
                    columns_str = step.split("for")[-1].strip().strip("'")
                    columns = [col.strip() for col in columns_str.split(",")]
                    current_data = fill_missing_values(current_data,"mean",columns)
                    try:
                        current_data = current_data[columns].mean(axis=0)
                    except KeyError as e:
                        print(f"{e}")
                elif step.startswith("median for"):
                    columns_str = step.split("for")[-1].strip().strip("'")
                    columns = [col.strip() for col in columns_str.split(",")]
                    current_data = fill_missing_values(current_data,"median",columns)
                    try:
                        current_data = current_data[columns].median(axis=0)
                    except KeyError as e:
                        print(f"{e}")
                elif step.startswith("mode for"):
                    columns_str = step.split("for")[-1].strip().strip("'")
                    columns = [col.strip() for col in columns_str.split(",")]
                    current_data = fill_missing_values(current_data,"mode",columns)
                    try:
                        current_data = current_data[columns].mode().iloc[0]  # Assuming mode returns multiple modes
                    except KeyError as e:
                        print(f"{e}")
                elif step == "remove rows with null":
                    current_data = remove_rows_with_null(current_data)
                elif step.startswith("rename column"):
                    parts = step.split(" ")
                    if len(parts) == 5 and parts[0] == 'rename' and parts[1] == 'column' and parts[3] == 'to':
                        old_name = parts[2]
                        new_name = parts[4]
                        try:
                            current_data = rename_column(current_data, old_name, new_name)
                            print(f"Column '{old_name}' renamed to '{new_name}'")
                        except KeyError as e:
                            print(f"{e}")
                        else:
                            print(f"Column '{old_name}' not found")
                elif step.startswith("view first"):
                    try:
                        num = int(step.split(" ")[-1])
                        print(current_data.head(num))
                    except:
                        print(f"{e}")
                elif step.startswith("view last"):
                    try:
                        num = int(step.split(" ")[-1])
                        print(current_data.tail(num))
                    except Exception as e:
                        print(f"{e}")
                elif step.startswith("save"):
                    save_var_name = step.split(" ")[-1].strip()
                    variables[save_var_name] = current_data
                    print(f"Data saved as '{save_var_name}'")
                elif step == 'output':
                    print(current_data)

            variables[var_name] = current_data

        elif node[0] == "OUTPUT_COLUMNS":
            var_name = node[1]
            columns = node[2]
            if var_name in variables:
                try:
                    result = variables[var_name][columns]
                    print(result)
                except Exception as e:
                    print(f"Error displaying selected columns: {e}")
            else:
                print(f"Variable '{var_name}' not found")

        
