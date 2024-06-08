import ply.lex as lex
from lang import Lang


class ArithLexer:
    tokens: tuple = Lang.tokens
    literals = Lang.literals
    t_ignore = " "

    # States for multi-line comments
    states = (("multilinecomment", "exclusive"),)

    t_CONCAT = r"<>"

    def t_ComandosIniciais(self, t):
        r"ESCREVER"
        t.type = t.value
        return t

    def t_ENTRADA(self, t):
        r"ENTRADA"
        t.type = t.value
        return t

    def t_ALEATORIO(self, t):
        r"ALEATORIO"
        t.type = t.value
        return t

    def t_NUM(self, t):
        r"[0-9]+"
        t.value = int(t.value)
        return t

    def t_STR(self, t):
        r'\"([^\\"]|\\.)*\"'
        t.value = t.value[1:-1]
        t.value = t.value.replace('\\"', '"')
        return t

    def t_VARIAVEL(self, t):
        r"[a-z_][a-zA-Z0-9_]*(?:[!?])?"
        return t

    def t_NAME(self, t):
        r"[a-z_][a-zA-Z0-9_]*"
        return t

    def t_FUNCAO(self, t):
        r"FUNCAO"
        t.type = t.value
        return t

    def t_FIM(self, t):
        r"FIM"
        t.type = t.value
        return t

    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)

    def t_COMMENT(self, t):
        r"\-\-.*"
        pass

    def t_multilinecomment(self, t):
        r"\{\-"
        t.lexer.begin("multilinecomment")
        pass

    def t_multilinecomment_content(self, t):
        r"[^\-]+"
        pass

    def t_multilinecomment_end(self, t):
        r"\-\}"
        t.lexer.begin("INITIAL")

    def t_multilinecomment_newline(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)

    def t_multilinecomment_error(self, t):
        t.lexer.skip(1)

    def t_error(self, t):
        print(f"Unexpected token: [{t.value[0]}]")
        t.lexer.skip(1)

    def build(self) -> None:
        self.lexer = lex.lex(module=self)

    def input(self, string: str) -> None:
        self.lexer.input(string)

    def token(self):
        return self.lexer.token()
