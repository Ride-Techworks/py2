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
        """ComandosIniciais : ESCREVER escrever ';'
        | variavel ';'
        | FUNCAO funcao FIM
        | VARIAVEL '=' func_call ';'
        | VARIAVEL '=' ENTRADA '(' ')' ';'
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
        elif len(p) == 7 and p[3] == "ENTRADA":
            self._variables[p[1]] = input("Enter value: ")

            if self._variables[p[1]].isdigit():
                self._variables[p[1]] = int(self._variables[p[1]])

            p[0] = {"op": "declare", "var_name": p[1], "value": self._variables[p[1]]}
            print(p[0])
        else:
            p[0] = p[1]

    def p_escrever(self, p):
        "escrever : '(' expression ')'"
        p[0] = p[2]

    def p_variavel(self, p):
        """variavel : VARIAVEL '=' expression"""
        if len(p) == 4:
            self._variables[p[1]] = p[3]
            p[0] = {"op": "declare", "var_name": p[1], "value": p[3]}

    def p_expression(self, p):
        """expression : expression_ops
        | STR
        | VARIAVEL"""
        if isinstance(p[1], str) and p[1] in self._variables:
            p[0] = self._variables[p[1]]
        else:
            p[0] = p[1]

    def p_expression_ops(self, p):
        """expression_ops : expression_ops '+' expression_ops
        | expression_ops '-' expression_ops
        | expression_ops '*' expression_ops
        | expression_ops '/' expression_ops
        | expression_ops CONCAT expression_ops
        | '(' expression_ops ')'
        | NUM
        | STR
        | VARIAVEL"""

        if len(p) == 4:
            if p[2] == "<>":
                left = self.get_variable_or_value(p[1])
                right = self.get_variable_or_value(p[3])
                p[0] = str(left) + str(right)
            else:
                p[0] = self.handle_four_length_expression(p)
        else:
            p[0] = self.handle_other_length_expression(p)

    def handle_four_length_expression(self, p):
        if p[1] == "(":
            return p[2]
        else:
            left = self.get_variable_or_value(p[1])
            right = self.get_variable_or_value(p[3])
            if p[2] == "+":
                return left + right
            elif p[2] == "-":
                return left - right
            elif p[2] == "*":
                return left * right
            elif p[2] == "/":
                return left / right
            elif p[2] == "<>":
                return str(left) + str(right)
            else:
                return None

    def handle_other_length_expression(self, p):
        if isinstance(p[1], str) and p[1] in self._variables:
            return self._variables[p[1]]
        else:
            return p[1]

    def get_variable_or_value(self, p):
        return self._variables[p] if p in self._variables else p

    def p_expression_uminus(self, p):
        "expression_ops : '-' expression_ops %prec UMINUS"
        p[0] = -p[2]

    def p_funcao(self, p):
        """
        funcao : NAME '(' arg ')'
        """
        p[0] = {"op": "func_declare", "args": p[3], "func_name": p[1]}

    def p_func_call(self, p):
        """
        func_call : ALEATORIO '(' expression_ops ')'
        | ESCREVER '(' expression_ops ')'
        | ESCREVER '(' STR ')'
        """

        if p[1] == "ESCREVER":
            p[0] = {"func": "ESCREVER", "arg": p[3]}

        if p[1] == "ALEATORIO":
            p[0] = {"func": "ALEATORIO", "arg": p[3]}

    def p_arg(self, p):
        """
        arg : NAME
        | NAME ',' arg
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
        self._variables = variables
        self.lexer.input(input)
        return self.yacc.parse(lexer=self.lexer.lexer)
