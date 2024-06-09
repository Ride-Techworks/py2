from typing import Dict, Tuple, List, Any

import ply.lex as lex
from lang import Lang


class ArithLexer:
    tokens: List[str] = Lang.tokens
    literals: List[str] = Lang.literals
    t_ignore: str = Lang.t_ignore
    t_multilinecomment_ignore: str = Lang.t_multilinecomment_ignore

    # States for multi-line comments
    states: Tuple[Tuple[str, str]] = (("multilinecomment", "exclusive"),)

    function_names: Dict[str, str] = {
        "soma": "NAME",
        "soma2": "NAME",
        "area": "NAME",
        "area_retangulo": "NAME",
        "area_quadrado": "NAME",
        "fib": "NAME",
        "mais2": "NAME",
        "somatorio": "NAME",
        "map": "MAP",
        "fold": "FOLD",
    }

    t_CONCAT: str = r"<>"
    t_ATRIBUICAO: str = r'='
    t_PARENTESES_ESQ: str = r'\('
    t_PARENTESES_DIR: str = r'\)'
    t_COLCHETES_ESQ: str = r'\['
    t_COLCHETES_DIR: str = r'\]'
    t_FUNCAO: str = r'FUNCAO'
    t_FIM: str = r'FIM'
    t_PONTO_E_VIRGULA: str = r';'
    t_OPERADOR_ARITMETICO: str = r'\+|-|\*|/'

    def t_ComandosIniciais(self, t: Any) -> lex.LexToken:
        r"ESCREVER"
        t.type = t.value
        return t

    def t_ENTRADA(self, t: Any) -> lex.LexToken:
        r"ENTRADA"
        t.type = t.value
        return t

    def t_MAP(self, t: Any) -> lex.LexToken:
        r"MAP"
        t.type = t.value
        return t

    def t_FOLD(self, t: Any) -> lex.LexToken:
        r"FOLD"
        t.type = t.value
        return t

    def t_ALEATORIO(self, t: Any) -> lex.LexToken:
        r"ALEATORIO"
        t.type = t.value
        return t

    def t_NUM(self, t: Any) -> lex.LexToken:
        r'\d+'
        t.value = int(t.value)
        return t

    def t_STR(self, t: Any) -> lex.LexToken:
        r'".*?"'
        t.value = t.value[1:-1]  # Remove as aspas da string reconhecida
        return t

    def t_VARIAVEL(self, t: Any) -> lex.LexToken:
        r"[a-z_][a-zA-Z0-9_]*(?:[!?])?"
        t.type = self.function_names.get(t.value, "VARIAVEL")
        return t

    def t_NAME(self, t: Any) -> lex.LexToken:
        r"[a-z][a-z0-9]*"
        t.type = self.function_names.get(t.value, "NAME")
        return t

    def t_newline(self, t) -> None:
        r'\n+'

    def t_COMMENT(self, t: Any) -> None:
        r'\-\-.*|{-(.|\n)*?-}'
        pass

    def t_multilinecomment(self, t: Any) -> None:
        r"\{\-"
        t.lexer.begin("multilinecomment")
        pass

    def t_multilinecomment_content(self, t: Any) -> None:
        r"[^\-]+"
        pass

    def t_multilinecomment_end(self, t: Any) -> None:
        r"\-\}"
        t.lexer.begin("INITIAL")

    def t_multilinecomment_newline(self, t: Any) -> None:
        r"\n+"
        t.lexer.lineno += len(t.value)

    def t_multilinecomment_error(self, t: Any) -> None:
        t.lexer.skip(1)

    def t_error(self, t: Any) -> None:
        print(f"Unexpected token: [{t.value[0]}]")
        t.lexer.skip(1)

    def build(self) -> None:
        self.lexer = lex.lex(module=self)

    def input(self, string: str) -> None:
        self.lexer.input(string)

    def token(self) -> lex.LexToken:
        return self.lexer.token()