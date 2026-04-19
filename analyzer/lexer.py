import re

class Token:
    def __init__(self, type_, value, line):
        self.type = type_
        self.value = value
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, '{self.value}', Line {self.line})"

class Lexer:
    def __init__(self):
        self.rules = [
            (r'\n', 'NEWLINE'),
            (r'[ \t]+', 'WHITESPACE'),
            (r'//.*', 'COMMENT'),
            (r'/\*.*?\*/', 'BLOCK_COMMENT'),
            (r'\bint\b', 'TYPE_INT'),
            (r'\bfloat\b', 'TYPE_FLOAT'),
            (r'\bstring\b', 'TYPE_STRING'),
            (r'\bif\b', 'IF'),
            (r'\belse\b', 'ELSE'),
            (r'\bwhile\b', 'WHILE'),
            (r'\breturn\b', 'RETURN'),
            (r'[a-zA-Z_][a-zA-Z0-9_]*', 'IDENTIFIER'),
            (r'[0-9]+\.[0-9]+', 'FLOAT_LIT'),
            (r'[0-9]+', 'INT_LIT'),
            (r'"[^"]*"', 'STRING_LIT'),
            (r'\+', 'PLUS'),
            (r'-', 'MINUS'),
            (r'\*', 'MULTIPLY'),
            (r'/', 'DIVIDE'),
            (r'==', 'EQEQ'),
            (r'=', 'EQUALS'),
            (r';', 'SEMICOLON'),
            (r'\(', 'LPAREN'),
            (r'\)', 'RPAREN'),
            (r'\{', 'LBRACE'),
            (r'\}', 'RBRACE'),
        ]
    
    def tokenize(self, code):
        tokens = []
        issues = []
        line_num = 1
        pos = 0
        
        # Compile rules
        regex_parts = []
        for regex, name in self.rules:
            regex_parts.append(f'(?P<{name}>{regex})')
        lexer_regex = re.compile('|'.join(regex_parts), re.DOTALL)
        
        while pos < len(code):
            match = lexer_regex.match(code, pos)
            if match:
                type_ = match.lastgroup
                value = match.group(type_)
                
                if type_ == 'NEWLINE':
                    line_num += 1
                elif type_ in ['WHITESPACE', 'COMMENT', 'BLOCK_COMMENT']:
                    pass # ignore
                else:
                    tokens.append(Token(type_, value, line_num))
                
                # Advance pos, update line numbers for multi-line block comments
                if type_ == 'BLOCK_COMMENT':
                    line_num += value.count('\n')
                    
                pos = match.end()
            else:
                # Unrecognized character
                char = code[pos]
                issues.append({
                    "severity": "error",
                    "category": "Lexical",
                    "line": line_num,
                    "message": f"Lexical Error: Unrecognized character '{char}'",
                    "fix": "Remove or correct the invalid character."
                })
                # Skip the bad character to continue lexing
                if char == '\n':
                    line_num += 1
                pos += 1
                
        return tokens, issues
