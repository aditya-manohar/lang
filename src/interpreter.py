from custom_builtins.data_loader import load_data
from custom_builtins.data_cleaner import clean_data,remove_rows,remove_columns
from custom_builtins.helper import execute_block

variables = {}

def interpret(ast):
    for node in ast:
        if node[0] == "STRING":
            print(node[1])  # Print string directly

        elif node[0] == "EXPRESSION":
            expression = node[1]
            try:
                # Handle expressions with comma (",") for concatenation
                if isinstance(expression, list):
                    result = []
                    for part in expression:
                        part = part.strip()  # Remove extra spaces around parts
                        if part.startswith('"') and part.endswith('"'):  # Handle strings
                            result.append(part[1:-1])  # Remove the quotes around string
                        elif part in variables:  # Handle variables
                            result.append(str(variables[part]))  # Convert variable to string
                        else:
                            raise NameError(f"Variable or string {part} not recognized.")
                    print("".join(result))  # Concatenate the parts without spaces
                    continue

                # Evaluate arithmetic expressions like a + b, a - c, etc.
                if "+" in expression or "-" in expression or "*" in expression or "/" in expression or "%" in expression or "**" in expression:
                    for var in variables:
                        expression = expression.replace(var, str(variables[var]))  # Replace vars with their values
                    result = eval(expression)  # Evaluate arithmetic expressions directly
                    print(result)
                    continue

                else:
                    # Handle single variable or literal expressions
                    if expression in variables:
                        print(variables[expression])  # Output the value of the variable
                    else:
                        print(expression)  # Output the expression as is
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
                        variables[var_name] = remove_columns(variables[var_name], custom_value)
                        print(f"cleaned using {strategy} column {custom_value}")
                    else:
                        variables[var_name] = clean_data(variables[var_name], strategy, custom_value)
                except Exception as e:
                    print(f"Error cleaning data in '{var_name}' : {e}")
            else:
                print(f"Variable '{var_name}' not found")

        elif node[0] == "SPLIT":
            data = variables.get('data')
            ratio = node[2]
            train_data,test_data = split_data(data,ratio)
            variables['train_data'] = train_data
            variables['test_data'] = test_data 

        
