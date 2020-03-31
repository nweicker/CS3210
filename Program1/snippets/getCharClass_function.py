# return the CharClass for a character
def get_CharClass(i):
    if i.isalpha():
        return CharClass.LETTER
    if i.isdigit():
        return CharClass.DIGIT
    if i in ['+', '-', '*', '/', '||', '&&', '==']:
        return CharClass.OPERATOR
    if i in ['.', ';']:
        return CharClass.PUNCTUATOR
#    if i in ["'", '"']:
#        return CharClass.QUOTE
    if i in ['\n', '\t', ' ']:
        return CharClass.BLANK
    if i in [",", "{", "}", "(", ")", "|", "/", "\\"]:
        return CharClass.DELIMITER
    return CharClass.OTHER