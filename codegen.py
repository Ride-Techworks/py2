class CodeGenerator:
    def __init__(self):
        self.code = []

    def generate(self, node):
        if node.type == "program":
            for child in node.children:
                self.generate(child)
        elif node.type == "assignment":
            value = self.generate(node.children[0])
            self.code.append(f"{node.value} = {value};")
        elif node.type == "binop":
            left = self.generate(node.children[0])
            right = self.generate(node.children[1])
            return f"({left} {node.value} {right})"
        elif node.type == "number":
            return str(node.value)
        elif node.type == "string":
            return node.value
        elif node.type == "variable":
            return node.value
        elif node.type == "list":
            return (
                "[" + ", ".join(self.generate(child) for child in node.children) + "]"
            )
        elif node.type == "escrever":
            value = self.generate(node.children[0])
            self.code.append(f'printf("{value}\\n");')
        elif node.type == "function":
            params = ", ".join(node.children[0])
            body = "\n".join(self.generate(statement) for statement in node.children[1])
            self.code.append(f"void {node.value}({params}) {{\n{body}\n}}")
        elif node.type == "function_call":
            args = ", ".join(self.generate(arg) for arg in node.children)
            self.code.append(f"{node.value}({args});")
        else:
            raise Exception(f"Unknown node type: {node.type}")

    def get_code(self):
        return "\n".join(self.code)


# Test the code generator
if __name__ == "__main__":
    from grammar import Parser

    parser = Parser()
    codegen = CodeGenerator()

    data = """
    ESCREVER("Hello, World!");
    a = 3 + 4 * 10;
    b = a / 2;
    ESCREVER(a);
    FUNCAO soma(a, b): a + b;
    """
    ast = parser.parse(data)
    codegen.generate(ast)
    print(codegen.get_code())
