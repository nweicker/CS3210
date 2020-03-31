
# TODO: change the hard-coded numbers to reference the enumerations

symbols = {
    "(": (Token.OPEN_PAR, 7),
    ")": (Token.CLOSE_PAR, 9),
    "{": (Token.OPEN_CURLY, 8),
    "}": (Token.CLOSE_CURLY, 7),
    "[": (Token.OPEN_BRACKET, 15),
    "]": (Token.CLOSE_BRACKET, 13),
    ",": (Token.COMMA, 21),
    "=": (Token.ASSIGNMENT, 18),
    ";": (Token.SEMICOLON, 17),
    "==": (Token.EQUALITY, ),
    "!=": (Token.INEQUALITY, ),
    "<": (Token.LESS, 20),
    "<=": (Token.LESS_EQUAL, 20),
    ">": (Token.GREATER, 20),
    ">=": (Token.GREATER_EQUAL, 20),
    "+": (Token.ADD, 20),
    "-": (Token.SUBTRACT, 20),
    "*": (Token.MULTIPLY, 20),
    "/": (Token.DIVIDE, 20),

    "int": (Token.INT_TYPE, 12),
    "int_lit": (Token.INT_LITERAL, 14),
    "main": (Token.MAIN, 11)
}