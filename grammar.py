import random
from pprint import PrettyPrinter
from typing import Any, Dict, Tuple, List

from utils import Utils
from lexer import ArithLexer
import ply.yacc as yacc

pp: PrettyPrinter = PrettyPrinter()


class ArithGrammar:
    tokens: List[str] = ArithLexer.tokens

    _variables: Dict[str, Any] = {}

    precedence: Tuple[Tuple[str, ...], ...] = (
        ("left", "CONCAT"),
        ("left", "OPERADOR_ARITMETICO"),
        ("right", "UMINUS"),
    )

    def p_Rec0(self, p: Any) -> None:
        "Rec : Start"
        p[0] = [p[1]]

    def p_Rec1(self, p: Any) -> None:
        "Rec : Rec Start"
        p[0] = p[1]
        p[0].append(p[2])

    def p_Start(self, p: Any) -> None:
        """Start : ComandosIniciais"""
        p[0] = p[1]

    def p_ComandosIniciais(self, p: Any) -> None:
        """
        ComandosIniciais : ESCREVER escrever PONTO_E_VIRGULA
            | variavel PONTO_E_VIRGULA
            | FUNCAO funcao FIM
            | FUNCAO funcao PONTO_E_VIRGULA
            | VARIAVEL ATRIBUICAO func_call PONTO_E_VIRGULA
            | VARIAVEL ATRIBUICAO ENTRADA PARENTESES_ESQ PARENTESES_DIR PONTO_E_VIRGULA
            | VARIAVEL ATRIBUICAO list PONTO_E_VIRGULA
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
            self._variables[p[1]] = random.randint(0, 10)
            p[0] = {
                "op": "declare",
                "var_name": p[1],
                "body": body,
                "value": self._variables[p[1]],
            }

        elif len(p) == 4 and p[1] == "ESCREVER":
            if isinstance(p[2], list):
                print(p[2])
            elif isinstance(p[2], str) and Utils.has_interpolation(p[2]):
                string = Utils.replace_interpolation(p[2], self._variables)
                p[0] = {"op": "print", "value": p[2]}
                print(string)
            else:
                p[0] = {"op": "print", "value": p[2]}

        elif len(p) == 7 and p[3] == "ENTRADA":
            self._variables[p[1]] = input("Enter value: ")

            if self._variables[p[1]].isdigit():
                self._variables[p[1]] = int(self._variables[p[1]])

            p[0] = {"op": "declare", "var_name": p[1], "value": self._variables[p[1]]}
        elif len(p) == 5 and p[2] == "=":

            self._variables[p[1]] = p[3]
            p[0] = {"op": "declare", "var_name": p[1], "value": p[3]}

        else:
            p[0] = p[1]

    def p_escrever(self, p: Any) -> None:
        "escrever : PARENTESES_ESQ expression PARENTESES_DIR"
        p[0] = p[2]

    def p_variavel(self, p: Any) -> None:
        """variavel : VARIAVEL ATRIBUICAO expression"""
        if len(p) == 4:
            self._variables[p[1]] = p[3]
            p[0] = {"op": "declare", "var_name": p[1], "value": p[3]}

    def p_expression(self, p: Any) -> None:
        """
        expression : expression_ops
            | STR
            | VARIAVEL
            | func_call
            | list
            | map_expr
            | fold_expr
        """
        if isinstance(p[1], str) and p[1] in self._variables:
            p[0] = self._variables[p[1]]
        elif p[1] is None:
            p[0] = 0
        else:
            p[0] = p[1]

    def p_expression_ops(self, p: Any) -> None:
        """
        expression_ops : expression_ops OPERADOR_ARITMETICO expression_ops
            | expression_ops CONCAT expression_ops
            | PARENTESES_ESQ expression_ops PARENTESES_DIR
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

    def p_map_expr(self, p: Any) -> None:
        "map_expr : MAP PARENTESES_ESQ NAME ',' expression PARENTESES_DIR"
        p[0] = {"op": "map", "func": p[3], "list": p[5]}

    def p_fold_expr(self, p: Any) -> None:
        "fold_expr : FOLD PARENTESES_ESQ NAME ',' expression ',' expression PARENTESES_DIR"
        p[0] = {"op": "fold", "func": p[3], "initial": p[5], "list": p[7]}

    def p_expressao_uminus(self, p: Any) -> None:
        "expression_ops : OPERADOR_ARITMETICO expression_ops %prec UMINUS"
        p[0] = {"op": "UMINUS", "value": p[2]}

    def p_list(self, p: Any) -> None:
        """
        list : COLCHETES_ESQ elements COLCHETES_DIR
             | COLCHETES_ESQ COLCHETES_DIR
        """
        if len(p) == 3:
            p[0] = []
        else:
            p[0] = p[2]

    def p_elements(self, p: Any) -> None:
        """
        elements : element
                 | element ',' elements
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]

    def p_element(self, p: Any) -> None:
        """element : expression"""
        p[0] = p[1]

    def p_funcao(self, p: Any) -> None:
        """
        funcao : NAME PARENTESES_ESQ arg PARENTESES_DIR ',' ':' func_call
            | NAME PARENTESES_ESQ arg PARENTESES_DIR ',' ':' expression_ops
            | NAME PARENTESES_ESQ arg PARENTESES_DIR ':' blocks
        """
        p[0] = {
            "op": "func_declare",
            "func_name": p[1],
            "args": p[3],
            "body": p[7] if len(p) == 8 else p[6],
        }

    def p_blocks(self, p: Any) -> None:
        """
        blocks : block
            | blocks block
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_block(self, p: Any) -> None:
        """
        block : variavel PONTO_E_VIRGULA
            | expression_ops PONTO_E_VIRGULA
            | func_call PONTO_E_VIRGULA
        """
        p[0] = p[1]

    def p_func_call(self, p: Any) -> None:
        """
        func_call : ALEATORIO PARENTESES_ESQ expression_ops PARENTESES_DIR
            | ESCREVER PARENTESES_ESQ expression_ops PARENTESES_DIR
            | ESCREVER PARENTESES_ESQ STR PARENTESES_DIR
            | NAME PARENTESES_ESQ arg PARENTESES_DIR
        """
        p[0] = {"func_call": p[1], "args": p[3]}

    def p_arg(self, p: Any) -> None:
        """
        arg : expression_ops
            | expression_ops ',' arg
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]

    def p_error(self, p: Any) -> None:
        print("Syntax error at '%s'" % p.value if p else "Syntax error at EOF")

    def build(self) -> None:
        self.lexer: ArithLexer = ArithLexer()
        self.lexer.build()
        self.yacc: yacc.LRParser = yacc.yacc(module=self)

    def parse(self, input: str, variables: Dict[str, Any]) -> Any:
        self._variables = variables
        self.lexer.input(input)
        return self.yacc.parse(lexer=self.lexer.lexer)