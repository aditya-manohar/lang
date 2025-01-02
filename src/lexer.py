import re

def lex(code):
    tokens = []
    lines = code.splitlines()
    for line_num, line in enumerate(lines, start=1):
        line = line.strip()

        if not line:
            continue

        print(f"Processing line {line_num}: {line}") 

        if line.startswith('input'):
            tokens.append(('INPUT', 'input'))
            line = line[len('input'):].strip()
            if line.isidentifier():
                tokens.append(('ID', line))
            else:
                raise RuntimeError(f"Unrecognized statement on line {line_num}")

        elif line.startswith("output"):
            match = re.match(r"output (.+)", line)
            if match:
                value = match.group(1).strip()
                if ',' in value:
                    parts = value.split(',')
                    tokens.append(("EXPRESSION", [part.strip() for part in parts]))
                elif value.startswith("'") and value.endswith("'"):
                    tokens.append(("STRING_SINGLE", value[1:-1]))
                elif value.startswith('"') and value.endswith('"'):
                    tokens.append(("STRING_DOUBLE", value[1:-1]))
                elif value.startswith("type(") and value.endswith(")"):
                    tokens.append(("TYPE", value[5:-1].strip()))  # Extract variable name inside type()
                else:
                    tokens.append(("EXPRESSION", value))
            else:
                raise RuntimeError(f"Invalid syntax on line {line_num}")

        elif line.startswith("if"):
            condition_match = re.match(r"if (.+?) then",line)
            if condition_match:
                condition = condition_match.group(1).strip()
                tokens.append(("IF",condition))
            else:
                raise RuntimeError(f"Invalid if syntax on line {line_num}")
                
        elif line == '(':
            tokens.append(("OPEN_BLOCK",None))

        elif line == ')':
            tokens.append(("CLOSE_BLOCK",None))
        
        elif line.startswith("else"):
            tokens.append(("ELSE",None))
            
        elif line.startswith("load"):
            match = re.match(r"load\s+'(.+?)'\s+as\s+(\w+)",line)
            if match:
                file_path = match.group(1)
                var_name = match.group(2)
                tokens.append(("LOAD",file_path,var_name))
            else:
                raise RuntimeError(f"Invalid load syntax on line {line_num}")
            
        elif line.startswith("clean"):
            match = re.match(r"clean (\w+) using (.+)", line)
            if match:
                var_name = match.group(1).strip()
                strategy = match.group(2).strip()

                if strategy == "remove duplicates":
                    tokens.append(("CLEAN", var_name, "remove duplicates", None))
                elif strategy in ["mean", "median", "mode"]:
                    tokens.append(("CLEAN", var_name, strategy, None))
                elif strategy.startswith("remove rows"):
                    condition = strategy.split("where")[-1].strip()
                    tokens.append(("CLEAN", var_name, "remove rows", condition))
                elif strategy.startswith("remove columns"):
                    columns = strategy.split("columns")[-1].strip()
                    columns = [col.strip() for col in columns.split(',')]
                    tokens.append(("CLEAN", var_name, "remove columns", columns))
                elif strategy.startswith("custom"):
                    custom_match = re.match(r"custom = (.+)", strategy)
                    if custom_match:
                        custom_value = custom_match.group(1).strip()
                        tokens.append(("CLEAN", var_name, "custom", custom_value))
            else:
                raise RuntimeError(f"Invalid clean syntax on line {line_num}")

        elif "->" in line:
            steps = [step.strip() for step in line.split("->")]
            var_name = steps[0]
            steps = steps[1:]

            parsed_steps = []
            for step in steps:
                if step.startswith("remove columns"):
                    match = re.match(r"remove columns (.+)",step)
                    if match:
                        columns = match.group(1).strip().split(',')
                        columns = [col.strip() for col in columns]
                        parsed_steps.append(("REMOVE_COLUMNS",columns))
                    else:
                        raise RuntimeError(f"Invalid remove column syntax")
                else:
                    parsed_steps.append(step)

            tokens.append(("CHAIN",var_name,steps))

        elif '=' in line:
            var_name, value = map(str.strip, line.split('=', 1))
            if not var_name.isidentifier():
                raise RuntimeError(f"Invalid variable name on line {line_num}")
            if value.isdigit():
                tokens.append(("SET", var_name, "NUMBER", int(value)))
            elif re.match(r"^\d+\.\d+$", value):  # Check for float
                tokens.append(("SET", var_name, "FLOAT", float(value)))
            elif value == "true":
                tokens.append(("SET", var_name, "BOOLEAN", True))
            elif value == "false":
                tokens.append(("SET", var_name, "BOOLEAN", False))
            elif value.startswith('"') and value.endswith('"'):
                tokens.append(("SET", var_name, "STRING", value[1:-1]))
            elif value.startswith("'") and value.endswith("'"):
                tokens.append(("SET", var_name, "STRING", value[1:-1]))
            # elif value.startswith('load '): 
            #     filename = value[len('load '):].strip()
            #     print(filename)
            #     if filename.startswith("'") and filename.endswith("'"):
            #         tokens.append(("SET",var_name,"LOAD",filename[1:-1]))
            #     else:
            #         raise RuntimeError(f"Invalid file name for 'load' on line {line_num}")
            # else:
            #     raise RuntimeError(f"Unsupported value type on line {line_num}")

        elif re.match(r"^\w+\s+\S+", line):
            var_name, value = line.split(maxsplit=1)
            if not var_name.isidentifier():
                raise RuntimeError(f"Invalid variable name on line {line_num}")
            if value.isdigit():
                tokens.append(("SET", var_name, "NUMBER", int(value)))
            elif re.match(r"^\d+\.\d+$", value):
                tokens.append(("SET", var_name, "FLOAT", float(value)))
            elif value == "true":
                tokens.append(("SET", var_name, "BOOLEAN", True))
            elif value == "false":
                tokens.append(("SET", var_name, "BOOLEAN", False))
            elif value.startswith('"') and value.endswith('"'):
                tokens.append(("SET", var_name, "STRING", value[1:-1]))
            elif value.startswith("'") and value.endswith("'"):
                tokens.append(("SET", var_name, "STRING", value[1:-1]))
            else:
                raise RuntimeError(f"Unsupported value type on line {line_num}")

    print(f"Generated tokens: {tokens}") 
    return tokens