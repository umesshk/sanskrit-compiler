from ast_nodes import *

def execute(ast):
    memory = {}

    def eval_expr(node):
        if isinstance(node, Num):
            return node.value

        if isinstance(node, Str):
            return node.value

        if isinstance(node, Var):
            return memory.get(node.name, 0)

        if isinstance(node, BinOp):
            l = eval_expr(node.left)
            r = eval_expr(node.right)

            if node.op == "PLUS": return l + r
            if node.op == "MINUS": return l - r
            if node.op == "MUL": return l * r
            if node.op == "DIV": return l // r
            if node.op == "GT": return l > r
            if node.op == "LT": return l < r

    def run_block(block):
        for stmt in block:
            run(stmt)

    def run(stmt):
        if isinstance(stmt, Assign):
            memory[stmt.name] = eval_expr(stmt.value)

        elif isinstance(stmt, Print):
            print(eval_expr(stmt.value))

        elif isinstance(stmt, If):
            if eval_expr(stmt.condition):
                run_block(stmt.body)
            else:
                run_block(stmt.else_body)

        elif isinstance(stmt, While):
            while eval_expr(stmt.condition):
                run_block(stmt.body)

    for stmt in ast:
        run(stmt)
