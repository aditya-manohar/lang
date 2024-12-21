def parse(tokens):
    ast = []
    token_iterator = iter(tokens)

    for token in token_iterator:
        if token[0] == "EXPRESSION":
            ast.append(("EXPRESSION", token[1]))
        elif token[0] in {"STRING_SINGLE", "STRING_DOUBLE"}:
            ast.append(("STRING", token[1]))
        elif token[0] == "SET":
            var_name = token[1]
            var_type = token[2]
            value = token[3]
            ast.append(("SET", var_name, var_type, value))
        elif token[0] == "INPUT":
            var_name = token[1]
            ast.append(("INPUT", var_name))
        elif token[0] == "TYPE":
            var_name = token[1]
            ast.append(("TYPE", var_name))  # Add type() expression to the AST
        elif token[0] == "ID":
            ast.append(("ID", token[1]))
        elif token[0] == "IF":
            condition = token[1]
            block = []
            while True:
                next_token = next(token_iterator)
                if next_token[0] == "OPEN_BLOCK":
                    continue
                elif next_token[0] == "CLOSE_BLOCK":
                    break
                else:
                    block.append(next_token)
            ast.append(("IF",condition,block))

        elif token[0] == "ELSE":
            block = []
            while True:
                next_token = next(token_iterator)
                if next_token[0] == "OPEN_BLOCK":
                    continue  
                elif next_token[0] == "CLOSE_BLOCK":
                    break 
                else:
                    block.append(next_token)
            ast.append(("ELSE", block))
            
        elif token[0] == "LOAD":
            file_path = token[1]
            var_name = token[2]
            ast.append(("LOAD",file_path,var_name))
        elif token[0] == "CLEAN":
            var_name = token[1]
            strategy = token[2]
            custom_value = token[3]
            ast.append(("CLEAN",var_name,strategy,custom_value))
        elif token[0] == "SPLIT":
            ast.append(("SPLIT",token[1],token[2]))
        else:
            raise SyntaxError(f"Unexpected token {token}")
    
    return ast


