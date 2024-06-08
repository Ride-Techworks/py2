import sys
from utils import Utils
from grammar import ArithGrammar
from codegen import CodeGenerator
from interpreter import Interpreter


def main():
    variables = {}
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>")
        return

    input_file = sys.argv[1]
    data = Utils.read_lang_file(input_file)

    parser = ArithGrammar()
    parser.build()
    interpreter = Interpreter()
    codegen = CodeGenerator()

    ast = parser.parse(data, variables)

    if ast is not None:
        # Interpret the input
        print(ast)

        # Generate C code
        """ interpreter.eval(ast)
        codegen.generate(ast)
        c_code = codegen.get_code()
        print("Generated C Code:")
        print(c_code) """
    else:
        print("Parsing failed.")


if __name__ == "__main__":
    main()
