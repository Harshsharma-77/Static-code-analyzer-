class Parser:
    def __init__(self):
        self.pos = 0
        self.tokens = []
        self.issues = []

    def parse(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.issues = []
        ast = []
        
        while self.pos < len(self.tokens):
            stmt = self.parse_statement()
            if stmt:
                ast.append(stmt)
            else:
                # If we couldn't parse a statement, try to recover by skipping to next semicolon
                self.recover()
        
        return ast, self.issues

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self, expected_type=None):
        tok = self.current()
        if expected_type:
            if tok and tok.type == expected_type:
                self.pos += 1
                return tok
            else:
                return None
        else:
            if tok:
                self.pos += 1
            return tok

    def recover(self):
        # Skip until semicolon or EOF to recover from an error
        while self.current() and self.current().type != 'SEMICOLON':
            self.pos += 1
        if self.current() and self.current().type == 'SEMICOLON':
            self.pos += 1

    def parse_statement(self):
        tok = self.current()
        if not tok:
            return None
            
        if tok.type in ['TYPE_INT', 'TYPE_FLOAT', 'TYPE_STRING']:
            return self.parse_declaration()
        elif tok.type == 'IDENTIFIER':
            return self.parse_assignment()
        elif tok.type in ['LBRACE', 'RBRACE', 'IF', 'WHILE', 'RETURN', 'ELSE']:
            # For simplicity in this demo, just skip block tokens and keywords to avoid huge parser
            self.pos += 1
            return {"node": "BlockOrControl", "value": tok.value, "line": tok.line}
        elif tok.type == 'SEMICOLON':
            self.pos += 1
            return None # empty statement
        else:
            # Unexpected token at statement level
            self.issues.append({
                "severity": "error",
                "category": "Syntax",
                "line": tok.line,
                "message": f"Syntax Error: Unexpected token '{tok.value}'",
                "fix": "Check for missing semicolons or invalid statement start."
            })
            self.pos += 1
            return None

    def parse_declaration(self):
        type_tok = self.consume() # TYPE_INT, TYPE_FLOAT, TYPE_STRING
        ident_tok = self.consume('IDENTIFIER')
        
        if not ident_tok:
            line = type_tok.line if type_tok else 0
            self.issues.append({
                "severity": "error",
                "category": "Syntax",
                "line": line,
                "message": "Syntax Error: Expected identifier after type declaration",
                "fix": "Provide a variable name."
            })
            return None

        # Check for assignment
        eq_tok = self.consume('EQUALS')
        expr = None
        if eq_tok:
            expr = self.parse_expression()
            if not expr:
                self.issues.append({
                    "severity": "error",
                    "category": "Syntax",
                    "line": eq_tok.line,
                    "message": "Syntax Error: Expected expression after '='",
                    "fix": "Provide a valid expression."
                })
        
        semi = self.consume('SEMICOLON')
        if not semi:
            prev = ident_tok if not eq_tok else (self.tokens[self.pos-1] if self.pos > 0 else ident_tok)
            self.issues.append({
                "severity": "error",
                "category": "Syntax",
                "line": prev.line,
                "message": "Syntax Error: Missing semicolon",
                "fix": "Add ';' at the end of the statement."
            })

        # map token types to semantic types
        type_str = "int"
        if type_tok.type == "TYPE_FLOAT": type_str = "float"
        elif type_tok.type == "TYPE_STRING": type_str = "string"

        return {
            "node": "Declaration",
            "var_type": type_str,
            "var_name": ident_tok.value,
            "expr": expr,
            "line": type_tok.line
        }

    def parse_assignment(self):
        ident_tok = self.consume('IDENTIFIER')
        eq_tok = self.consume('EQUALS')
        if not eq_tok:
            # Might just be an expression statement, for simplicity treat as error if not assignment
            self.issues.append({
                "severity": "error",
                "category": "Syntax",
                "line": ident_tok.line,
                "message": f"Syntax Error: Expected '=' after '{ident_tok.value}'",
                "fix": "Complete the assignment statement."
            })
            return None
            
        expr = self.parse_expression()
        semi = self.consume('SEMICOLON')
        if not semi:
            self.issues.append({
                "severity": "error",
                "category": "Syntax",
                "line": eq_tok.line,
                "message": "Syntax Error: Missing semicolon",
                "fix": "Add ';' at the end of the statement."
            })
            
        return {
            "node": "Assignment",
            "var_name": ident_tok.value,
            "expr": expr,
            "line": ident_tok.line
        }

    def parse_expression(self):
        # A very simplified expression parser, just grabbing the first value/identifier for type checking demo
        tok = self.current()
        if not tok:
            return None
            
        if tok.type in ['INT_LIT', 'FLOAT_LIT', 'STRING_LIT', 'IDENTIFIER']:
            self.pos += 1
            # Skip optional math ops for simplicity
            while self.current() and self.current().type in ['PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE']:
                self.pos += 1
                if self.current() and self.current().type in ['INT_LIT', 'FLOAT_LIT', 'STRING_LIT', 'IDENTIFIER']:
                    self.pos += 1
                else:
                    break
            
            # We return the primary token of the expression for type inference
            return {
                "node": "Expression",
                "type": tok.type,
                "value": tok.value,
                "line": tok.line
            }
        return None
