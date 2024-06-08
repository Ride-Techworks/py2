class Lang:
    tokens = (
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
    )
    literals = (
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
    t_ignore = " \n\t"
    t_multilinecomment_ignore = " \t"
