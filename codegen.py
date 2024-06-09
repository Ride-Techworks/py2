class CodeGen:
    def __init__(self):
        self.code = []
        self.variables = {}

    def generate(self, parsed_data):
        self.code.append("#include <stdio.h>")
        self.code.append("int main() {")
        for statement in parsed_data:
            self.code.append("    " + self._generate_statement(statement) + ";")
        self.code.append("    return 0;")
        self.code.append("}")
        return "\n".join(self.code)

    def _generate_statement(self, statement):
        if statement['op'] == 'print':
            return f'printf("%d\\n", {self._generate_expression(statement["value"])})'
        elif statement['op'] == 'declare':
            if statement["var_name"] not in self.variables:
                self.variables[statement["var_name"]] = "int"
            return f'int {statement["var_name"]} = {self._generate_expression(statement["value"])}'
        elif statement['op'] == 'func_declare':
            func_args = ", ".join(f"int {arg}" for arg in statement['args'])
            func_body = ";\n    ".join(self._generate_statement(line) for line in statement['body'])
            return f'int {statement["func_name"]}({func_args}) {{\n    {func_body};\n}}'
        elif statement['op'] == 'map':
            return f'map({statement["func"]}, {self._generate_expression(statement["list"])})'
        elif statement['op'] == 'fold':
            return f'fold({statement["func"]}, {self._generate_expression(statement["initial"])}, {self._generate_expression(statement["list"])})'
        return ""

    def _generate_expression(self, expression):
        if isinstance(expression, dict):
            if expression['op'] == 'UMINUS':
                return f'-{self._generate_expression(expression["value"])}'
            return f'({self._generate_expression(expression["left"])} {expression["op"]} {self._generate_expression(expression["right"])})'
        return str(expression)