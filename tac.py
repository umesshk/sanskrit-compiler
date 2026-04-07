from ast_nodes import Num, Var, BinOp, Assign, Print

temp_count = 0

def new_temp():
    global temp_count
    temp_count += 1
    return f"t{temp_count}"

def generate_TAC(node, code):
    if isinstance(node, Num):
        return str(node.value)

    if isinstance(node, Var):
        return node.name

    if isinstance(node, BinOp):
        left = generate_TAC(node.left, code)
        right = generate_TAC(node.right, code)
        temp = new_temp()
        code.append(f"{temp} = {left} {node.op} {right}")
        return temp

    if isinstance(node, Assign):
        val = generate_TAC(node.value, code)
        code.append(f"{node.name} = {val}")

    if isinstance(node, Print):
        val = generate_TAC(node.value, code)
        code.append(f"PRINT {val}")
