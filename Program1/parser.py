# CS 3210 - Project 1
# Authors:
#   Nicole Weickert
#   Myke Walker

import sys
from enum import IntEnum
import re       # regular expressions

# TODO: remove import and put code in parser file
#from Program1.lex import *

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
def error_message(code=""):

    # prevent errors from missing or non-numeric error codes
    if type(code) is not int or not code:
        code = 99

    raise Exception(errors[code])


# receives text and separates it into a list of valid words
def get_lexemes(text, word="", lexemes=[]):

    # stop recursion at end of text;  add word if it exists
    if len(text) == 0:
        if word:
            lexemes.append(word)
        return lexemes

    # end words at spaces
    if text[0] in "\n \t \r":
        if word:
            lexemes.append(word)
            word = ""

    # continue words for alphanumeric characters
    elif text[0].isalnum():
        word += text[0]

    # check for 2-symbol operators  NOTE:
    elif text[0:2] in ("==", "!=", "<=", ">=", "&&", "||"):
        lexemes.append(text[0:2])
        text = text[1:]

    # add symbols as their own lexemes
    # (reference the lexeme table in case a symbol is changed later)
    elif text[0] in lex_table.keys():
        if word:
            lexemes.append(word)
            word = ""
        lexemes.append(text[0])

    else:
        return "Unrecognized character"
#    print("", text, " ", "", word, "", lexemes)
    return get_lexemes(text[1:], word, lexemes)


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

    lexemes = get_lexemes(file_contents)
    for n in lexemes:
        print(n)
