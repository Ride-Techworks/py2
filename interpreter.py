class Interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}

    def eval(self, node):
        if node.type == 'program':
            for child in node.children:
                self.eval(child)
        elif node.type == 'assignment':
            self.variables[node.value] = self.eval(node.children[0])
        elif node.type == 'binop':
            left = self.eval(node.children[0])
            right = self.eval(node.children[1])
            if node.value == '+':
                return left + right
            elif node.value == '-':
                return left - right
            elif node.value == '*':
                return left * right
            elif node.value == '/':
                return left / right
        elif node.type == 'number':
            return node.value
        elif node.type == 'string':
            return node.value
        elif node.type == 'variable':
            return self.variables.get(node.value, 0)
        elif node.type == 'list':
            return [self.eval(child) for child in node.children]
        elif node.type == 'escrever':
            value = self.eval(node.children[0])
            print(value)
        elif node.type == 'function':
            self.functions[node.value] = node
        elif node.type == 'function_call':
            func = self.functions.get(node.value)
            if not func:
                raise Exception(f"Function {node.value} not defined")
            params = func.children[0]
            body = func.children[1]
            local_vars = {params[i]: self.eval(node.children[i]) for i in range(len(params))}
            old_vars = self.variables
            self.variables = local_vars
            for stmt in body:
                self.eval(stmt)
            result = self.variables.get('return')
            self.variables = old_vars
            return result
        else:
            raise Exception(f"Unknown node type: {node.type}")

# Test the interpreter
if __name__ == "__main__":
    from grammar import Parser
    parser = Parser()
    interpreter = Interpreter()

    data = '''
    ESCREVER("Hello, World!");
    a = 3 + 4 * 10;
    b = a / 2;
    ESCREVER(a);
    FUNCAO soma(a, b): a + b;
    '''
    ast = parser.parse(data)
    interpreter.eval(ast)
    print(interpreter.variables)
