def get_token(lexeme=""):

    # check for empty
    if lexeme == "":
        return Token.EOF

    # if lexeme is a number, return type
    if type(lexeme) is int:
        return Token.INT_LITERAL
    if type(lexeme) is float:
        return Token.FLOAT_LITERAL

    # if lexeme is in the symbol dictionary
    if lexeme in symbols:
        return  symbols[lexeme]

    # if lexeme is one letter in single quotes
    if lexeme[0] == lexeme[-1] == "'" \
            and lexeme[1].isalpha() \
            and len(lexeme) == 3:
        return Token.CHAR_LITERAL

    # if lexeme starts with a letter...
    if lexeme[0].isalpha():

        # keywords (token name is the same as the lexeme)
        if lexeme in ("main", "if", "else", "while", "or", "and",
                      "true", "false",
                      "assignment", "identifier"):
            return Token[lexeme.upper()]

        # variable types (token name is partial match to lexeme)
        if lexeme in ("int", "bool", "float", "char"):
            i = (lexeme.upper() + "_TYPE")
            return Token[i]


    return "NOT RECOGNIZED"