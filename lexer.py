import re

KEYWORDS = {
    "यदि": "IF",
    "तदा": "THEN",
    "अथ": "ELSE",
    "निर्गम": "PRINT",
    "किन्चित्काल": "WHILE"
}

TOKENS = [
  ("STRING", r'"[^"]*"'),
    ("NUMBER", r"\d+"),
   ("ID", r"[a-zA-Z\u0900-\u097F]+"),
    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("MUL", r"\*"),
    ("DIV", r"/"),
    ("EQ", r"="),
    ("GT", r">"),
    ("LT", r"<"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("SEMI", r";"),
]

def tokenize(code):
    tokens = []
    i = 0

    while i < len(code):
        if code[i].isspace():
            i += 1
            continue

        match = None

        for token_type, pattern in TOKENS:
            regex = re.compile(pattern)
            match = regex.match(code, i)

            if match:
                value = match.group(0)

                if value in KEYWORDS:
                    tokens.append((KEYWORDS[value], value))
                else:
                    tokens.append((token_type, value))

                i = match.end()
                break

        if not match:
            raise Exception(f"Invalid character: {code[i]}")

    return tokens
