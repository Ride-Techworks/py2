import re
from lexer import ArithLexer
import re
from lexer import ArithLexer
import ply.yacc as yacc
from pprint import PrettyPrinter
import random
from utils import Utils

pp = PrettyPrinter()


class ArithGrammar:
    tokens = ArithLexer.tokens

    _variables = {}

    precedence = (
        ("left", "CONCAT"),
        ("left", "+", "-"),
        ("left", "*", "/"),
        ("right", "UMINUS"),
    )

    def p_Rec0(self, p):
        "Rec : Start"
        p[0] = [p[1]]

    def p_Rec1(self, p):
        "Rec : Rec Start"
        p[0] = p[1]
        p[0].append(p[2])

    def p_Start(self, p):
        """Start : ComandosIniciais"""
        p[0] = p[1]

    def p_ComandosIniciais(self, p):
        """
        ComandosIniciais : ESCREVER escrever ';'
            | variavel ';'
            | FUNCAO funcao FIM
            | FUNCAO funcao ';'
            | VARIAVEL '=' func_call ';'
            | VARIAVEL '=' ENTRADA '(' ')' ';'
            | VARIAVEL '=' list ';'
        """
        if len(p) == 4 and p[1] != "ESCREVER":
            p[0] = p[2]
        elif len(p) == 5 and isinstance(p[3], dict) and p[3].get("func") == "ALEATORIO":
            self._variables[p[1]] = random.randint(0, p[3]["arg"])
            p[0] = {"op": "declare", "var_name": p[1], "value": self._variables[p[1]]}
        elif len(p) == 4 and p[1] == "ESCREVER":
            if Utils.has_interpolation(str(p[2])):
                interpolated = Utils.replace_interpolation(p[2], self._variables)
                p[0] = {"op": "print", "value": p[2]}
                print(interpolated)
            else:
                p[0] = {"op": "print", "value": p[2]}
                print(p[2])

        elif (
            len(p) == 5
            and isinstance(p[3], dict)
            and p[3].get("func_call") == "ALEATORIO"
        ):
            body = p[3]
            self._variaveis[p[1]] = random.randint(0, 10)
            p[0] = {
                "op": "declare",
                "var_name": p[1],
                "body": body,
                "value": self._variaveis[p[1]],
            }

        elif len(p) == 4 and p[1] == "ESCREVER":
            if isinstance(p[2], list):
                print(p[2])
            elif isinstance(p[2], str) and Utils.has_interpolation(p[2]):
                string = Utils.replace_interpolation(p[2], self._variaveis)
                p[0] = {"op": "print", "value": p[2]}
                print(string)
            else:
                p[0] = {"op": "print", "value": p[2]}

        elif len(p) == 7 and p[3] == "ENTRADA":
            self._variaveis[p[1]] = input("Enter value: ")

            if self._variaveis[p[1]].isdigit():
                self._variaveis[p[1]] = int(self._variaveis[p[1]])

            p[0] = {"op": "declare", "var_name": p[1], "value": self._variaveis[p[1]]}
        elif len(p) == 5 and p[2] == "=":

            self._variaveis[p[1]] = p[3]
            p[0] = {"op": "declare", "var_name": p[1], "value": p[3]}

        else:
            p[0] = p[1]

    def p_escrever(self, p):
        "escrever : '(' expression ')'"
        p[0] = p[2]

    def p_variavel(self, p):
        """variavel : VARIAVEL '=' expression"""
        if len(p) == 4:
            self._variaveis[p[1]] = p[3]
            p[0] = {"op": "declare", "var_name": p[1], "value": p[3]}

    def p_expression(self, p):
        """
        expression : expression_ops
            | STR
            | VARIAVEL
            | func_call
            | list
        """
        if isinstance(p[1], str) and p[1] in self._variaveis:
            p[0] = self._variaveis[p[1]]
        elif p[1] is None:
            p[0] = 0
        else:
            p[0] = p[1]

    def p_expression_ops(self, p):
        """
        expression_ops : expression_ops '+' expression_ops
            | expression_ops '-' expression_ops
            | expression_ops '*' expression_ops
            | expression_ops '/' expression_ops
            | expression_ops CONCAT expression_ops
            | '(' expression_ops ')'
            | NUM
            | STR
            | VARIAVEL
        """
        if len(p) == 4:
            p[0] = {"op": p[2], "left": p[1], "right": p[3]}
        elif len(p) == 3 and p[1] == "(" and p[3] == ")":
            p[0] = p[2]
        else:
            p[0] = p[1]

    def p_expressao_uminus(self, p):
        "expression_ops : '-' expression_ops %prec UMINUS"
        p[0] = {"op": "UMINUS", "value": p[2]}

    def p_list(self, p):
        """
        list : '[' elements ']'
            | '[' ']'
        """
        if len(p) == 3:
            p[0] = []
        else:
            p[0] = p[2]

    def p_elements(self, p):
        """
        elements : element
            | element ',' elements
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]

    def p_element(self, p):
        """element : expression"""
        p[0] = p[1]

    def p_funcao(self, p):
        """
        funcao : NAME '(' arg ')' ',' ':' func_call
            | NAME '(' arg ')' ',' ':' expression_ops
            | NAME '(' arg ')' ':' blocks
        """
        p[0] = {
            "op": "func_declare",
            "func_name": p[1],
            "args": p[3],
            "body": p[7] if len(p) == 8 else p[6],
        }

    def p_blocks(self, p):
        """
        blocks : block
            | blocks block
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_block(self, p):
        """
        block : variavel ';'
            | expression_ops ';'
            | func_call ';'
        """
        p[0] = p[1]

    def p_func_call(self, p):
        """
        func_call : ALEATORIO '(' expression_ops ')'
            | ESCREVER '(' expression_ops ')'
            | ESCREVER '(' STR ')'
            | NAME '(' arg ')'
        """
        p[0] = {"func_call": p[1], "args": p[3]}

    def p_arg(self, p):
        """
        arg : expression_ops
            | expression_ops ',' arg
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]

    def p_error(self, p):
        print("Syntax error at '%s'" % p.value if p else "Syntax error at EOF")

    def build(self):
        self.lexer = ArithLexer()
        self.lexer.build()
        self.yacc = yacc.yacc(module=self)

    def parse(self, input, variables):
        self._variaveis = variables
        self.lexer.input(input)
        return self.yacc.parse(lexer=self.lexer.lexer)
