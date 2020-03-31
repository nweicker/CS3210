from Program1.parser import *

# receives a value and returns its token ID or error code (default token)
def lex_lookup(lexeme, code="token"):

    # quit if code is invalid
    if code not in ("token", "error"):
        raise IndexError

    # if the lexeme is in the list, return its token or error code
    if lexeme in lex_table.keys():
        if code == "token":
            return Token(lex_table[lexeme][0])
        else:
            return lex_table[lexeme][1]

    # if the lexeme isn't in the list, compare to the literal patterns
    else:
        # Token.IDENTIFIER      <letter> { <letter> | <digit> }
        # Token.INT_LITERAL     <digit> { <digit> }
        # Token.FLOAT_LITERAL   <int_literal> . <int_literal>
        # Token.CHAR_LITERAL    ' <letter> '

        patterns = [
            (Token.IDENTIFIER, "[a-z][a-z|0-9]*", 16),
            (Token.INT_LITERAL, "[0-9]+", 14),
            (Token.FLOAT_LITERAL, "[0-9]+\.[0-9]+", 4),
            (Token.CHAR_LITERAL, "\'[a-z]\'", 5)
        ]

        # compare lexeme (as a string) against the regex for each pattern
        for i in patterns:
            if bool(re.fullmatch(i[1], str(lexeme))):
                if code == "token":
                    return i[0]
                else:
                    return i[2]

       # if no match, return lexical error
        error_message(3)

