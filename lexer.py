import ply.lex as lex
from lang import Lang


class Lexer(Lang):
    def __init__(self):
        self.lexer = None

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def input(self, data):
        self.lexer.input(data)

    def token(self):
        return self.lexer.token()


# Test the lexer
if __name__ == "__main__":
    lexer = Lexer()
    lexer.build()
    data = """
    ESCREVER("Hello, World!");
    a = 3 + 4 * 10;
    b = a / 2;
    c = "Hello" <> "World";
    FUNCAO soma(a, b): a + b; FIM
    """
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
