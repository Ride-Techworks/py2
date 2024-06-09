import random

from grammar import ArithGrammar


class Interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}

    def eval(self, node):
        if isinstance(node, list):
            results = []
            for child in node:
                results.append(self.eval(child))
            return results
        elif isinstance(node, dict):
            if node['op'] == 'declare':
                self.variables[node['var_name']] = self.eval(node['value'])
            elif node['op'] == 'print':
                value = self.eval(node['value'])
                print(value)
            elif node['op'] == 'func_declare':
                self.functions[node['func_name']] = node
            elif node['op'] == 'func_call':
                func = self.functions.get(node['func_call'])
                if not func:
                    raise Exception(f"Function {node['func_call']} not defined")
                params = func['args']
                body = func['body']
                local_vars = {params[i]: self.eval(node['args'][i]) for i in range(len(params))}
                old_vars = self.variables
                self.variables = local_vars
                result = None
                if isinstance(body, list):
                    for stmt in body:
                        result = self.eval(stmt)
                else:
                    result = self.eval(body)
                self.variables = old_vars
                return result
            elif node['op'] in {'+', '-', '*', '/'}:
                left = self.eval(node['left'])
                right = self.eval(node['right'])
                if node['op'] == '+':
                    return left + right
                elif node['op'] == '-':
                    return left - right
                elif node['op'] == '*':
                    return left * right
                elif node['op'] == '/':
                    return left / right
            elif node['op'] == 'map':
                func = self.functions.get(node['func'])
                if not func:
                    raise Exception(f"Function {node['func']} not defined")
                lst = self.eval(node['list'])
                if lst is None:
                    lst = []
                return [self.eval({'op': 'func_call', 'func_call': node['func'], 'args': [item]}) for item in lst]
            elif node['op'] == 'fold':
                func = self.functions.get(node['func'])
                if not func:
                    raise Exception(f"Function {node['func']} not defined")
                result = self.eval(node['initial'])
                for item in self.eval(node['list']):
                    result = self.eval({'op': 'func_call', 'func_call': node['func'], 'args': [result, item]})
                return result
            elif isinstance(node, dict) and node.get('func') == 'ALEATORIO':
                return random.randint(0, node['args'])
            elif isinstance(node, dict) and 'value' in node:
                return node['value']
        elif isinstance(node, int) or isinstance(node, str):
            return node
        else:
            raise Exception(f"Unknown node type: {node}")


def main():
    input_code = """
    FUNC mais2(x) : x + 2;
    FUNC soma(a, b) : a + b;
    lista1 = MAP(mais2, []);
    lista2 = MAP(mais2, [1, 2, 3]);
    lista3 = FOLD(soma, 0, [1, 2, 3]);
    ESCREVER(MAP(mais2, [1, 2, 3]));
    ESCREVER(FOLD(soma, 0, [1, 2, 3]));
    """

    # Initialize the parser
    parser = ArithGrammar()
    parser.build()

    # Parse the input code
    parsed_code = parser.parse(input_code, {})

    # Initialize the interpreter
    interpreter = Interpreter()

    # Evaluate the parsed code
    interpreter.eval(parsed_code)

if __name__ == "__main__":
    main()

