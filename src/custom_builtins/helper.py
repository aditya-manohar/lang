def execute_block(ast, start_index):
    for i in range(start_index, len(ast)):
        node = ast[i]
        if node[0] in {"ENDIF", "ELSE"}:
            break
        interpret([node])  # Recurse into the block
