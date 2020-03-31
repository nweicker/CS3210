# break the input text into words and symbols
def get_lexemes(text, word="", lexemes=[]):
    # stop recursion at end of input
    if len(text) == 0:
        if len(word) > 0:
            lexemes.append(word)
        return lexemes

    # if char is symbol, append previous word and symbol; clear word
    elif get_CharClass(text[0]) in range(3, 9):

        # do not append empty words
        if len(word) > 0:
            lexemes.append(word)

        # do not append blank characters
        if get_CharClass(text[0]) != 6:

            # check for 2-character operators
            if text[0:2] in ("==", "!=", "<=", ">="):
                lexemes.append(text[0:2])
                text = text[1:]
            else:
                lexemes.append(text[0])

        # clear word
        word = ""

    # if char is alphanumeric or _, increase word
    else:
        word = word + text[0]

    # reduce text by first letter and repeat
    text = text[1:]
    return get_lexemes(text, word, lexemes)