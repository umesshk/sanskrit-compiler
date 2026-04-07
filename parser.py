from ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def eat(self, type_):
        token = self.current()
        if token and token[0] == type_:
            self.pos += 1
            return token
        raise Exception(f"Expected {type_}, got {token}")

    def parse(self):
        stmts = []
        while self.current():
            stmts.append(self.statement())
        return stmts

    def statement(self):
        tok = self.current()

        if tok[0] == "ID":
            return self.assignment()

        elif tok[0] == "PRINT":
            return self.print_stmt()

        elif tok[0] == "IF":
            return self.if_stmt()

        elif tok[0] == "WHILE":
            return self.while_stmt()

        else:
            raise Exception("Invalid statement")

    def block(self):
        stmts = []
        self.eat("LBRACE")
        while self.current()[0] != "RBRACE":
            stmts.append(self.statement())
        self.eat("RBRACE")
        return stmts

    def if_stmt(self):
        self.eat("IF")
        cond = self.expr()
        self.eat("THEN")
        body = self.block()

        else_body = []
        if self.current() and self.current()[0] == "ELSE":
            self.eat("ELSE")
            else_body = self.block()

        self.eat("SEMI")
        return If(cond, body, else_body)

    def while_stmt(self):
        self.eat("WHILE")
        cond = self.expr()
        self.eat("THEN")
        body = self.block()
        self.eat("SEMI")
        return While(cond, body)

    def assignment(self):
        name = self.eat("ID")[1]
        self.eat("EQ")
        val = self.expr()
        self.eat("SEMI")
        return Assign(name, val)

    def print_stmt(self):
        self.eat("PRINT")
        val = self.expr()
        self.eat("SEMI")
        return Print(val)

    def expr(self):
        left = self.term()

        while self.current() and self.current()[0] in ("PLUS","MINUS","GT","LT"):
            op = self.eat(self.current()[0])[0]
            right = self.term()
            left = BinOp(left, op, right)

        return left

    def term(self):
        left = self.factor()

        while self.current() and self.current()[0] in ("MUL","DIV"):
            op = self.eat(self.current()[0])[0]
            right = self.factor()
            left = BinOp(left, op, right)

        return left

    def factor(self):
        tok = self.current()

        if tok[0] == "NUMBER":
            return Num(self.eat("NUMBER")[1])

        if tok[0] == "STRING":
            return Str(self.eat("STRING")[1].strip('"'))

        if tok[0] == "ID":
            return Var(self.eat("ID")[1])

        if tok[0] == "LPAREN":
            self.eat("LPAREN")
            e = self.expr()
            self.eat("RPAREN")
            return e

        raise Exception("Invalid expression")
