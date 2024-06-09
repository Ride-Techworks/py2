import sys
from utils import Utils
from grammar import ArithGrammar
from codegen import CodeGen
from interpreter import Interpreter

def main():
    variaveis = {}
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>")
        return

    input_file = sys.argv[1]
    data = Utils.read_lang_file(input_file)

    parser = ArithGrammar()
    parser.build()
    interpreter = Interpreter()
    codegen = CodeGen()

    ast = parser.parse(data, variaveis)

    if ast is not None:
        # Interpret the input
        print("AST:")
        print(ast)
        print("\nInterpreted Output:")
        interpreter = Interpreter()
        interpreter.eval(ast)

        # Generate Python code
        generated_code = codegen.generate(ast)
        print("\nGenerated C Code:")
        print(generated_code)
    else:
        print("Parsing failed.")

if __name__ == "__main__":
    main()
