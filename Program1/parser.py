# CS 3210 - Project 1
# Authors:
#   Nicole Weickert
#   Myke Walker

# squash traceback reporting on errors
# sys.tracebacklimit = 0

import sys
from enum import IntEnum
import re       # regular expressions

#### Lookup Tables #####################################################
class Token(IntEnum):
# Token table from specifications
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

errors = {
# Error Table from Specifications
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
lookup_table = {
# Symbol-Token-Error Join Table
    # (each value is a tuple of the key's (token id, error code)
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
regex_patterns = {
    # float must come before integer or partial matches may be inaccurate
    "IDENTIFIER": "[a-z|A-Z][a-z|A-Z|0-9]*",
    "FLOAT_LITERAL": "[0-9]+\.[0-9]+",
    "INT_LITERAL": "[0-9]+",
    "CHAR_LITERAL": "\'[a-z|A-Z]\'"
}
keywords = ["int", "main", "if", "else", "while", "bool", "float",
            "char", "true", "false"]


#### Functions #########################################################
def add_tuple(list, text):
    if text in lookup_table.keys():
        list.append((lookup(text), text))

    elif bool(pattern_match(text)):
        token = str(Token[pattern_match(text)])
        list.append((token, text))
    return list

def error_message(code=None):
# receives error code and calls an error with the appropriate message

    # prevent errors from missing, non-numeric, or invalid error codes
    if not code in errors.keys():
        code = 99
    raise Exception(errors[code])
    quit()

def lookup(expression, column=""):

    record = lookup_table.get(expression)

    if column == "error":
        print("error_message(",record[1],")")
    else:
        return  str(Token(record[0]))

def pattern_match(expression, partial=False):
#   Evaluate input and return the name of a matching pattern (or None)
#
#   Partial (optional)
#       By default, the function requires an exact match to the whole string.
#       If 'partial' is True, it will allow a partial match from the start
#       Partial returns the name of the pattern AND its length.

    # compare against all patterns, return the first match or None
    match = None
    for pattern in regex_patterns.items():
        if not partial:
            if bool(re.fullmatch(pattern[1], expression)):
                # on full match, return pattern name
                match = pattern[0]
                break
        else:
            for key in keywords:
                if re.match(key, expression):
                    match = key[1], len(key[1])
                break

            # check for a partial match starting from first character
            partial_match = (re.match(pattern[1], expression))

            # save the matching substring (without whitespace) as partial_match
            if partial_match:
                partial_match = partial_match.group(0).rstrip()

                # return pattern name and length of matching substring
                match = (pattern[0], len(partial_match))
                break
    return match

def split_list_item(list, text):

    if text[0:2] in lookup_table.keys():
        list = add_tuple(list, text[0:2])
        text = text[2:]

    elif text[0] in lookup_table.keys():
        list = add_tuple(list, text[0])
        text = text[1:]
    return list, text

def text_to_tokens(text):
    lexemes = text.split()
    tokens = []

    # Loop through list
    i = -1
    while i < len(lexemes)-1:
        i += 1
        text = lexemes[i]

        # for items that match a Token key or pattern, replace with tuple
        if text in lookup_table.keys() or \
           bool(pattern_match(text)):
            tokens = add_tuple(tokens, text)
            continue

        # for items that don't match a Token or pattern, split into smaller units
        else:
            while len(text) > 0:
                partial = pattern_match(text, True)
                if bool(partial):
                    tokens.append((str(Token[partial[0]]), text[0:partial[1]]))
                    text = text[partial[1]:]
                else:
                    list, text = split_list_item(tokens, text)
    tokens.append((str(Token.EOF), "$"))
    return tokens

#### Parse Tree ########################################################
class Tree:
# structure the parse tree

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


#########  Main ########################################################
if __name__ == "__main__":

    # Check for source file
    if len(sys.argv) != 2:
        error_message(1)
    source = open(sys.argv[1], "rt")
    if not source:
        error_message(2)
    file_contents = source.read()
    source.close()

    tree = text_to_tokens(file_contents)

    for token in tree:
        print(token)