from typing import Tuple


class Lang:
    tokens: Tuple[str, ...] = (
        "ATRIBUICAO",
        "NUM",
        "VARIAVEL",
        "STR",
        "FUNCAO",
        "FIM",
        "NAME",
        "ALEATORIO",
        "ESCREVER",
        "ENTRADA",
        "CONCAT",
        "PARENTESES_ESQ",
        "PARENTESES_DIR",
        "OPERADOR_ARITMETICO",
        "PONTO_E_VIRGULA",
        'COLCHETES_ESQ',
        'COLCHETES_DIR',
        'MAP',
        'FOLD',
    )
    literals: Tuple[str, ...] = (
        "(",
        ")",
        "*",
        "+",
        "=",
        ";",
        '"',
        ",",
        ":",
        "?",
        "!",
        "-",
        "_",
        "{",
        "}",
        "<",
        ">",
        "#",
        "[",
        "]",
    )
    t_ignore: str = " \n\t"
    t_multilinecomment_ignore: str = " \t"
