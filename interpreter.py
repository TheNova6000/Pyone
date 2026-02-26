"""
Pyone DSL Interpreter
Version: 1.0.0
Author: Sri Krishna Batkeeri
Description:
A minimal English-based DSL interpreter with stack-based evaluation.
"""


import sys
class Pyone:
    def __init__(self):
        self.variables = {}

    def code(self, s):
        lines = [line.strip() for line in s.splitlines() if line.strip()]

        i = 0
        while i < len(lines):
            line = lines[i]
            token = line.split()

            # ---------- declaration ----------
            if token[0] == "let":
                self.decleration(line)
                i += 1
                continue 
            if token[0] == "if":
                # --- find block structure ---
                elif_lines = []
                else_line = None
                end_line = None

                j = i + 1
                while j < len(lines):
                    if lines[j].startswith("otherwise"):
                        elif_lines.append(j)
                    elif lines[j] == "else":
                        else_line = j
                    elif lines[j] == "end":
                        end_line = j
                        break
                    j += 1

                if end_line is None:
                    raise SyntaxError("if without end")

                # all control markers
                markers = sorted(
                    elif_lines +
                    ([else_line] if else_line is not None else []) +
                    [end_line]
                )

                def next_marker(after):
                    for m in markers:
                        if m > after:
                            return m
                    return end_line

                branch_start = None
                branch_end = None

                # ---------- IF condition ----------
                cond_text = lines[i][3:]
                clean, temp = self.preprocess_expression(cond_text)
                if self.exp_eval(clean, temp):
                    branch_start = i + 1
                    branch_end = next_marker(i)

                # ---------- OTHERWISE (elif) ----------
                if branch_start is None:
                    for k in elif_lines:
                        cond = lines[k][10:]
                        clean, temp = self.preprocess_expression(cond)
                        if self.exp_eval(clean, temp):
                            branch_start = k + 1
                            branch_end = next_marker(k)
                            break

                # ---------- ELSE ----------
                if branch_start is None:
                    if else_line is not None:
                        branch_start = else_line + 1
                        branch_end = end_line
                    else:
                        i = end_line + 1
                        continue

                # ---------- EXECUTE SELECTED BRANCH ----------
                i = branch_start
                while i < branch_end:
                    inner = lines[i]
                    inner_tok = inner.split()

                    if inner_tok[0] == "let":
                        self.decleration(inner)

                    elif inner_tok[0] in self.variables and len(inner_tok) > 1 and inner_tok[1] in {"is", "be"}:
                        self.assignment(inner)

                    elif inner_tok[0] == "print":
                        self.block(inner)

                    elif inner_tok[0] == "if":
                        raise SyntaxError("Nested if not supported yet")

                    i += 1

                # ---------- jump past end ----------
                i = end_line + 1
                continue

            # ---------- markers (ignored at runtime) ----------
            if token[0] in {"otherwise", "else", "end"}:
                i += 1
                continue

            # ---------- assignment ----------
            elif (
                len(token) > 1
                and token[0] in self.variables
                and token[1] in {"is", "be"}):
                self.assignment(line)
                i += 1

            # ---------- else / end (markers only) ----------
            elif token[0] in {"else", "end"}:
                i += 1

            # ---------- block ----------
            else:
                self.block(line)
                i += 1

        print(self.variables)

    def decleration(self, line):

            parts = line.split(maxsplit=3)

            # --- Check number of parts ---
            if len(parts) < 4:
                raise SyntaxError(
                    "Invalid declaration syntax. Expected format: let <variable> is <expression>"
                )

            keyword, name, helping_verb, expression = parts


            # --- Check variable name ---
            if not name.isidentifier():
                raise SyntaxError(f"Invalid variable name: '{name}'")

            # --- Check helping verb ---
            if helping_verb not in {"is", "be"}:
                raise SyntaxError(
                    f"Invalid declaration keyword '{helping_verb}'. Use 'is' or 'be'"
                )

            # --- Check redeclaration ---
            if name in self.variables:
                raise SyntaxError(f"Variable '{name}' is already declared")

            # --- Evaluate expression ---
            clean_expr, temp = self.preprocess_expression(expression)
            value = self.exp_eval(clean_expr, temp)

            self.variables[name] = value

    def preprocess_expression(self, expression):
        placeholders = {}
        result = ""
        i = 0
        counter = 0

        while i < len(expression):
            ch = expression[i]


            # start of string literal
            if ch == '"' or ch == "'":
                quote = ch
                i += 1
                start = i

                while i < len(expression) and expression[i] != quote:
                    i += 1

                if i >= len(expression):
                    raise SyntaxError("Unterminated string literal")

                value = expression[start:i]
                key = f"__STR{counter}__"
                placeholders[key] = value
                result += key
                counter += 1
                i += 1  # skip closing quote

            else:
                result += ch
                i += 1
        replacements = [
            ("is greater than or equal to", ">="),
            ("is less than or equal to", "<="),
            ("is greater than", ">"),
            ("is less than", "<"),
            ("is equals to", "=="),]

        for phrase, symbol in replacements:
            result = result.replace(phrase, symbol)

        return result, placeholders

    def exp_eval(self, expression,temp_values=None):
        if temp_values is None:
            temp_values = {}
        stack = []

        for tok in expression.split():

            # number
            if tok.isdigit():
                stack.append(int(tok))

            # string literal (double quotes)
            elif tok.startswith('"') and tok.endswith('"'):
                stack.append(tok[1:-1])

            # string literal (single quotes)
            elif tok.startswith("'") and tok.endswith("'"):
                stack.append(tok[1:-1])
            #temp value for nested strings or multiple strings 
            elif tok in temp_values:
                stack.append(temp_values[tok])
            # variable
            elif tok in self.variables:
                stack.append(self.variables[tok])
            # operator
            elif tok == "+":
                if len(stack) < 2:
                    raise SyntaxError("Not enough operands for +")

                b = stack.pop()
                a = stack.pop()

                # type-safe addition
                if isinstance(a, int) and isinstance(b, int):
                    stack.append(a + b)
                elif isinstance(a, str) and isinstance(b, str):
                    stack.append(a + " " + b)
                else:
                    raise TypeError("Cannot add different data types")
            
            elif tok == "-":
                if len(stack) < 2:
                    raise SyntaxError("Not enough operands for Subtraction")

                b = stack.pop()
                a = stack.pop()

                # type-safe addition
                if isinstance(a, int) and isinstance(b, int):
                    stack.append(a - b)
            elif tok == "*":
                if len(stack) < 2:
                    raise SyntaxError("Not enough operands for multiplication")

                b = stack.pop()
                a = stack.pop()

                # type-safe addition
                if isinstance(a, int) and isinstance(b, int):
                    stack.append(a * b)
            elif tok == "/":
                if len(stack) < 2:
                    raise SyntaxError("Not enough operands for division")

                b = stack.pop()
                a = stack.pop()

                # type-safe addition
                if isinstance(a, int) and isinstance(b, int):
                    stack.append(a / b)
            elif tok == ">":
                if len(stack) < 2:
                    raise SyntaxError("Not enough operands for Comparison")

                b = stack.pop()
                a = stack.pop()

                # type-safe addition
                if isinstance(a, int) and isinstance(b, int):
                    stack.append(a > b)               
            elif tok == "<":
                if len(stack) < 2:
                    raise SyntaxError("Not enough operands for Comparision")

                b = stack.pop()
                a = stack.pop()

                # type-safe addition
                if isinstance(a, int) and isinstance(b, int):
                    stack.append(a < b) 
            elif tok == "<=":
                if len(stack) < 2:
                    raise SyntaxError("Not enough operands for Comparision")

                b = stack.pop()
                a = stack.pop()

                # type-safe addition
                if isinstance(a, int) and isinstance(b, int):
                    stack.append(a <= b) 
            elif tok == ">=":
                if len(stack) < 2:
                    raise SyntaxError("Not enough operands for Comparision")

                b = stack.pop()
                a = stack.pop()

                # type-safe addition
                if isinstance(a, int) and isinstance(b, int):
                    stack.append(a >= b) 
            elif tok == "==":

                if len(stack) < 2:
                    raise SyntaxError("Not enough operands for Comparision")

                b = stack.pop()
                a = stack.pop()

                # type-safe addition
                if isinstance(a, int) and isinstance(b, int):
                    stack.append(a == b) 


            else:
                raise SyntaxError(f"Unknown token: {tok}")

        # expression must produce exactly one value
        if len(stack) != 1:
            raise SyntaxError("Invalid expression")

        return stack[0]

    def block(self, line):

        parts = line.split(maxsplit=1)

        # --- Check structure ---
        if len(parts) < 2:
            raise SyntaxError(
                "Invalid block syntax. Expected format: print <expression>"
            )

        keyword, expression = parts

        # --- Check supported block keyword ---
        if keyword != "print":
            raise NotImplementedError(
                f"Block keyword '{keyword}' is not supported. "
                "Currently only 'print' block logic is implemented."
            )

        # --- Execute print ---
        clean_expr, temp = self.preprocess_expression(expression)
        print(self.exp_eval(clean_expr, temp))

    def assignment(self, line):

        parts = line.split(maxsplit=2)

        # --- Check structure ---
        if len(parts) < 3:
            raise SyntaxError(
                "Invalid assignment syntax. Expected format: <variable> is <expression>"
            )

        name, helping_verb, expression = parts

        # --- Check variable existence ---
        if name not in self.variables:
            raise NameError(
                f"Variable '{name}' is not declared. Use 'let {name} is ...' before assignment."
            )

        # --- Check helping verb ---
        if helping_verb not in {"is", "be"}:
            raise SyntaxError(
                f"Invalid assignment keyword '{helping_verb}'. Use 'is' or 'be'."
            )

        # --- Evaluate expression ---
        clean_expr, temp = self.preprocess_expression(expression)
        value = self.exp_eval(clean_expr, temp)

        self.variables[name] = value

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pyone.py <filename.pyo>")
        sys.exit(1)

    try:
        with open(sys.argv[1], "r") as f:
            Pyone().code(f.read())
    except FileNotFoundError:
        print("Error: File not found.")
    except Exception as e:
        print(f"Runtime Error: {e}")