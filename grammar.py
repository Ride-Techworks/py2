import ply.yacc as yacc
from lexer import Lexer  # Ensure this imports the correct Lexer class


class Node:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children or []

    def __repr__(self):
        return f"Node(type={self.type}, value={self.value}, children={self.children})"


class Parser:
    tokens = Lexer.tokens

    precedence = (
        ("left", "CONCAT"),
        ("left", "PLUS", "MINUS"),
        ("left", "TIMES", "DIVIDE"),
    )

    def __init__(self):
        self.lexer = Lexer()
        self.lexer.build()
        self.parser = yacc.yacc(module=self)

    def parse(self, data):
        return self.parser.parse(data, lexer=self.lexer.lexer)

    def p_program(self, p):
        """program : statement_list"""
        print("Parsing program")
        p[0] = Node("program", children=p[1])

    def p_statement_list(self, p):
        """statement_list : statement_list statement
        | statement
        | empty"""
        if len(p) == 2:
            if p[1] is not None:
                print("Parsing single statement")
                p[0] = [p[1]]
            else:
                print("Parsing empty statement list")
                p[0] = []
        else:
            print("Parsing statement list")
            p[0] = p[1] + [p[2]]

    def p_statement(self, p):
        """statement : assignment SEMI
        | statement_expr SEMI
        | function_declaration"""
        if len(p) == 3:
            print("Parsing statement with assignment or expression")
            p[0] = p[1]
        else:
            print("Parsing function declaration")
            p[0] = p[1]

    def p_statement_expr(self, p):
        """statement_expr : ESCREVER LPAREN expression RPAREN
        | ALEATORIO LPAREN NUM RPAREN
        | ENTRADA LPAREN RPAREN
        | function_call"""
        if p[1] == "ESCREVER":
            print("Parsing ESCREVER statement")
            p[0] = Node("escrever", children=[p[3]])
        elif p[1] == "ALEATORIO":
            print(f"Parsing ALEATORIO statement with max value: {p[3]}")
            p[0] = Node("aleatorio", value=p[3])
        elif p[1] == "ENTRADA":
            print("Parsing ENTRADA statement")
            p[0] = Node("entrada")
        else:  # Function call
            if len(p) == 5:  # Function call with arguments
                args = p[4]  # Access the argument list at p[4]
                print(
                    f"Parsing function call: {p[1]}({', '.join(str(arg) for arg in args)})"
                )
                p[0] = Node("function_call", value=p[1], children=args)
            else:  # Function call with no arguments
                print(f"Parsing function call: {p[1]}()")
                p[0] = Node("function_call", value=p[1], children=[])

    def p_assignment(self, p):
        """assignment : VARIAVEL EQUALS expression"""
        print(f"Parsing assignment: {p[1]} = {p[3]}")
        p[0] = Node("assignment", value=p[1], children=[p[3]])

    def p_expression(self, p):
        """expression : expr"""
        p[0] = p[1]

    def p_expr(self, p):
        """expr : expr PLUS term
        | expr MINUS term
        | expr CONCAT term
        | term"""
        if len(p) == 2:
            print("Parsing term in expression")
            p[0] = p[1]
        elif p[2] == "+":
            print(f"Parsing addition: {p[1]} + {p[3]}")
            p[0] = Node("binop", value="+", children=[p[1], p[3]])
        elif p[2] == "-":
            print(f"Parsing subtraction: {p[1]} - {p[3]}")
            p[0] = Node("binop", value="-", children=[p[1], p[3]])
        elif p[2] == "<>":
            print(f"Parsing concatenation: {p[1]} <> {p[3]}")
            p[0] = Node("concat", children=[p[1], p[3]])

    def p_term(self, p):
        """term : term TIMES factor
        | term DIVIDE factor
        | factor"""
        if len(p) == 2:
            print("Parsing factor in term")
            p[0] = p[1]
        elif p[2] == "*":
            print(f"Parsing multiplication: {p[1]} * {p[3]}")
            p[0] = Node("binop", value="*", children=[p[1], p[3]])
        elif p[2] == "/":
            print(f"Parsing division: {p[1]} / {p[3]}")
            p[0] = Node("binop", value="/", children=[p[1], p[3]])

    def p_factor(self, p):
        """factor : NUM
        | LPAREN expression RPAREN
        | STR
        | VARIAVEL
        | list"""
        if len(p) == 2:
            if isinstance(p[1], int) or isinstance(p[1], float):
                print(f"Parsing number: {p[1]}")
                p[0] = Node("number", value=p[1])
            elif isinstance(p[1], str) and p[1].startswith('"'):
                print(f"Parsing string: {p[1]}")
                p[0] = Node("string", value=p[1])
            else:
                print(f"Parsing variable: {p[1]}")
                p[0] = Node("variable", value=p[1])
        else:
            print("Parsing grouped expression")
            p[0] = p[2]

    def p_list(self, p):
        """list : LBRACKET elements RBRACKET"""
        print("Parsing list")
        p[0] = Node("list", children=p[2])

    def p_elements(self, p):
        """elements : expression
        | elements COMMA expression"""
        if len(p) == 2:
            print("Parsing single element in list")
            p[0] = [p[1]]
        else:
            print("Parsing multiple elements in list")
            p[0] = p[1] + [p[3]]

    # Function Declaration and Call Rules (Corrected)
    def p_function_declaration(self, p):
        """function_declaration : FUNCAO VARIAVEL LPAREN parameter_list RPAREN COLON statement_list FIM"""
        print(f"Parsing function declaration: {p[2]} with statements: {p[7]}")
        p[0] = Node("function", value=p[2], children=[p[4], p[7]])

    def p_function_call(self, p):
        """function_call : VARIAVEL LPAREN argument_list RPAREN"""
        print(f"Parsing function call: {p[1]}({', '.join(str(arg) for arg in p[3])})")
        p[0] = Node("function_call", value=p[1], children=p[3])

    def p_argument_list(self, p):
        """argument_list : expression
        | argument_list COMMA expression"""
        if len(p) == 2:
            print("Parsing single argument")
            p[0] = [p[1]]
        else:
            print("Parsing multiple arguments")
            p[0] = p[1] + [p[3]]

    def p_parameter_list(self, p):
        """parameter_list : VARIAVEL
        | parameter_list COMMA VARIAVEL"""
        if len(p) == 2:
            print("Parsing single parameter")
            p[0] = [p[1]]
        else:
            print("Parsing multiple parameters")
            p[0] = p[1] + [p[3]]

    def p_empty(self, p):
        "empty :"
        p[0] = None

    def p_error(self, p):
        if p:
            print(f"Syntax error at '{p.value}'")
            print(p)
        else:
            print("Syntax error at EOF")


if __name__ == "__main__":
    parser = Parser()
    data = """
    FUNCAO mais2( x ),: x + 2 ;
FUNCAO soma( a, b ),: a + b ;
lista1 = map( mais2, [] ); 		-- []
lista2 = map( mais2, [ 1, 2, 3 ] );  	-- = [ mais2(1),mais2(2),mais2(3)] = [3,4,5]
lista3 = fold( soma, [ 1, 2, 3 ], 0 );
			-- = soma( 1, soma(2, soma ( 3, 0)))
		    -- = soma( 1, soma(2, 3 ))
			-- = soma( 1, 5)
			-- = 6
    """
    result = parser.parse(data)
    if result:
        print("Parsing succeeded.")
        print(result)
    else:
        print("Parsing failed.")
