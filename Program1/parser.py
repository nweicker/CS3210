# CS 3210 - Project 1
# Authors:
#   Nicole Weickert
#   Myke Walker

import sys
from enum import IntEnum
import re       # regular expressions

# squash traceback reporting on errors
sys.tracebacklimit = 0

#######################################################################
#   Lookup Tables
#######################################################################

# Tokens
class Token(IntEnum):
    EOF = 0
    INT_TYPE = 1
    MAIN = 2
    OPEN_PAR = 3
    CLOSE_PAR = 4
    OPEN_CURLY = 5
    CLOSE_CURLY = 6
    OPEN_BRACKET = 7
    CLOSE_BRACKET = 8
    COMMA = 9
    ASSIGNMENT = 10
    SEMICOLON = 11
    IF = 12
    ELSE = 13
    WHILE = 14
    OR = 15
    AND = 16
    EQUALITY = 17
    INEQUALITY = 18
    LESS = 19
    LESS_EQUAL = 20
    GREATER = 21
    GREATER_EQUAL = 22
    ADD = 23
    SUBTRACT = 24
    MULTIPLY = 25
    DIVIDE = 26
    BOOL_TYPE = 27
    FLOAT_TYPE = 28
    CHAR_TYPE = 29
    IDENTIFIER = 30
    INT_LITERAL = 31
    TRUE = 32
    FALSE = 33
    FLOAT_LITERAL = 34
    CHAR_LITERAL = 35

# Errors
errors = {
    1: "Source file missing",
    2: "Couldn't open source file",
    3: "Lexical error",
    4: "Digit expected",
    5: "Symbol missing",
    6: "EOF expected",
    7: "'}' expected",
    8: "'{' expected",
    9: "')' expected",
    10: "'(' expected",
    11: "main expected",
    12: "int type expected",
    13: "']' expected",
    14: "int literal expected",
    15: "'[' expected",
    16: "identifier expected",
    17: "';' expected",
    18: "'=' expected",
    19: "identifier, if, or while expected",
    20: "operator expected",
    21: "',' expected",
    22: "else expected",
    23: "type expected",
    24: "boolean expected",
    99: "syntax error"
}

# Lexemes   (each value is a tuple of the key's (token id, error code)
lex_table = {
    "": (0, 6),
    "int": (1, 12),
    "main": (2, 11),
    "(": (3, 10),
    ")": (4, 9),
    "{": (5, 8),
    "}": (6, 7),
    "[": (7, 15),
    "]": (8, 13),
    ",": (9, 21),
    "=": (10, 18),
    ";": (11, 17),
    "if": (12, 19),
    "else": (13, 22),
    "while": (14, 19),
    "||": (15, 20),
    "&&": (16, 20),
    "==": (17, 20),
    "!=": (18, 20),
    "<": (19, 20),
    "<=": (20, 20),
    ">": (21, 20),
    ">=": (22, 20),
    "+": (23, 20),
    "-": (24, 20),
    "*": (25, 20),
    "/": (26, 20),
    "bool": (27, 23),
    "float": (28, 23),
    "char": (29, 23),
    "true": (32, 24),
    "false": (33, 24)
}

#######################################################################
#   Objects
#######################################################################

# structure the parse tree
class Tree:

    TAB = "   "

    def __init__(self):
        self.data = None
        self.children = []

    def add(self, child):
        self.children.append(child)

    def print(self, tab=""):
        if self.data is not None:
            print(tab + self.data)
            tab += self.TAB
            for child in self.children:
                if isinstance(child, Tree):
                    child.print(tab)
                else:
                    print(tab + child)

#######################################################################
#   Functions
#######################################################################

# error code to message conversion function with optional code number
def error_message(code=None):

    # prevent errors from missing or non-numeric error codes
    if type(code) is not int or not code:
        code = 99
    raise Exception(errors[code])


# receives text and separates it into a list of valid lexemes
def get_lexemes(text, word="", list=[]):

    # stop recursion at end of text;  add word if it exists
    if len(text) == 0:
        list.append(word)
        return list

    # end words at spaces
    if text[0] in (""," ", ' ', "\n", "\t", "\r"):
        list.append(word)
        word = ""
        print("word: ", word)

    # continue words for alphanumeric characters
    elif text[0].isalnum():
        word += text[0]

    # check for 2-symbol operators
    #   (note that the slice will not cause index error on length < 2)
    elif text[0:2] in ("==", "!=", "<=", ">=", "&&", "||"):

        # add word to list if it exists
        list.append(word)
        word = ""

        # add 2-character symbol to list
        list.append(text[0:2])

        # reduce text by an extra digit
        text = text[1:]

    # add symbols as their own lexemes
    # (reference the lexeme table in case a symbol is changed later)
    elif text[0].lower() in lex_table.keys():

        # add word to list (if it exists) and clear the word
        list.append(word)
        word = ""

        # add symbol to list
        list.append(text[0])

    else:
        return f"Unrecognized character: {text[0]}"

    # remove first character from text and repeat
    return get_lexemes(text[1:], word, list)


def lex_lookup(lexeme, code="token"):

    # quit if code is invalid
    if code not in ("token", "error"):
        raise Exception

    # if the lexeme is in the list, return its token or error code
    if lexeme in lex_table.keys():
        if code == "token":
            # return type is Token
            return Token(lex_table[lexeme][0])
        else:
            # no return
            error_message(lex_table[lexeme][1])

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
            # evaluates True if the string exactly matches the pattern
            if bool(re.fullmatch(i[1], str(lexeme))):
                if code == "token":
                    return i[0]
                else:
                    error_message(i[2])

       # if no match, return lexical error
        error_message(3)

#######################################################################
#   Main
#######################################################################
if __name__ == "__main__":

    # Check for source file
    if len(sys.argv) != 2:
        error_message(1)
    source = open(sys.argv[1], "rt")
    if not source:
        error_message(2)

    # The language is not case-sensitive so convert all to lowercase
    file_contents = source.read().lower()
    source.close()
