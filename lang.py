import ply.lex as lex


class Lang:
    tokens = (
        "ESCREVER",
        "ENTRADA",
        "ALEATORIO",
        "FUNCAO",
        "FIM",
        "NUM",
        "STR",
        "VARIAVEL",
        "CONCAT",
        "PLUS",
        "MINUS",
        "TIMES",
        "DIVIDE",
        "EQUALS",
        "LPAREN",
        "RPAREN",
        "SEMI",
        "LBRACKET",
        "RBRACKET",
        "COMMA",
        "COLON",
    )

    t_PLUS = r"\+"
    t_MINUS = r"-"
    t_TIMES = r"\*"
    t_DIVIDE = r"/"
    t_EQUALS = r"="
    t_LPAREN = r"\("
    t_RPAREN = r"\)"
    t_SEMI = r";"
    t_CONCAT = r"<>"
    t_LBRACKET = r"\["
    t_RBRACKET = r"\]"
    t_COMMA = r","
    t_COLON = r":"

    t_ignore = " \t"

    def t_ESCREVER(self, t):
        r"ESCREVER"
        return t

    def t_ENTRADA(self, t):
        r"ENTRADA"
        return t

    def t_ALEATORIO(self, t):
        r"ALEATORIO"
        return t

    def t_FUNCAO(self, t):
        r"FUNCAO"
        return t

    def t_FIM(self, t):
        r"FIM"
        return t

    def t_NUM(self, t):
        r"\d+"
        t.value = int(t.value)
        return t

    def t_STR(self, t):
        r"\"([^\\\n]|(\\.))*?\" "
        return t

    def t_VARIAVEL(self, t):
        r"[a-zA-Z_][a-zA-Z_0-9]*"
        return t

    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)
