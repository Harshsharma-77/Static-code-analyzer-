class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.issues = []

    def analyze(self, ast):
        self.symbol_table = {}
        self.issues = []

        # Pass 1: populate symbols, check declarations and types
        for node in ast:
            if not isinstance(node, dict):
                continue
                
            if node.get("node") == "Declaration":
                var_name = node["var_name"]
                var_type = node["var_type"]
                line = node["line"]
                
                if var_name in self.symbol_table:
                    self.issues.append({
                        "severity": "error",
                        "category": "Semantic",
                        "line": line,
                        "message": f"Semantic Error: Variable '{var_name}' is already declared.",
                        "fix": "Rename the variable or remove the duplicate declaration."
                    })
                else:
                    self.symbol_table[var_name] = {
                        "type": var_type,
                        "declared_line": line,
                        "used": False
                    }
                    
                # Type checking
                expr = node.get("expr")
                if expr:
                    self.check_type(var_name, var_type, expr, line)
                    self.mark_used(expr)
                    
            elif node.get("node") == "Assignment":
                var_name = node["var_name"]
                line = node["line"]
                
                if var_name not in self.symbol_table:
                    self.issues.append({
                        "severity": "error",
                        "category": "Semantic",
                        "line": line,
                        "message": f"Semantic Error: Variable '{var_name}' is used before declaration.",
                        "fix": f"Declare '{var_name}' before using it (e.g., 'int {var_name};')."
                    })
                else:
                    var_type = self.symbol_table[var_name]["type"]
                    expr = node.get("expr")
                    if expr:
                        self.check_type(var_name, var_type, expr, line)
                        self.mark_used(expr)

        # Pass 2: check for unused variables
        for var_name, info in self.symbol_table.items():
            if not info["used"]:
                self.issues.append({
                    "severity": "warning",
                    "category": "Code Quality",
                    "line": info["declared_line"],
                    "message": f"Warning: Variable '{var_name}' is declared but never used.",
                    "fix": f"Remove the declaration of '{var_name}' or use it."
                })

        return self.issues

    def mark_used(self, expr):
        if expr and expr["type"] == "IDENTIFIER":
            name = expr["value"]
            if name in self.symbol_table:
                self.symbol_table[name]["used"] = True
            else:
                self.issues.append({
                    "severity": "error",
                    "category": "Semantic",
                    "line": expr["line"],
                    "message": f"Semantic Error: Variable '{name}' is used before declaration.",
                    "fix": f"Declare '{name}' before using it."
                })

    def check_type(self, var_name, expected_type, expr, line):
        actual_type = expr["type"]
        val = expr["value"]
        
        # very basic type inference for demo
        inferred = None
        if actual_type == "INT_LIT": inferred = "int"
        elif actual_type == "FLOAT_LIT": inferred = "float"
        elif actual_type == "STRING_LIT": inferred = "string"
        elif actual_type == "IDENTIFIER":
            if val in self.symbol_table:
                inferred = self.symbol_table[val]["type"]
                self.symbol_table[val]["used"] = True
                
        if inferred and inferred != expected_type:
            # C allows int to float conversion, let's just make it strict for the demo or string to int error
            if (expected_type == "int" and inferred == "string") or \
               (expected_type == "string" and inferred in ["int", "float"]) or \
               (expected_type == "float" and inferred == "string"):
                self.issues.append({
                    "severity": "error",
                    "category": "Type Check",
                    "line": line,
                    "message": f"Type Mismatch: Cannot assign '{inferred}' to variable '{var_name}' of type '{expected_type}'.",
                    "fix": f"Ensure the assigned value is of type '{expected_type}'."
                })
