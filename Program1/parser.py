# CS 3210 - Project 1
# Authors:
#   Nicole Weickert
#   Myke Walker


import sys
from enum import IntEnum
import re       # regular expressions

# squash traceback reporting on errors
sys.tracebacklimit = 0

######### Lookup Tables ################################################
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
    SYNTAX_ERROR = 99

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
    "$": (0, 6),
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

######### Functions ####################################################
def check_terminals(grammar, tokens, tree):
# grammar: list of expected characters
# tokens, tree: the current state of the parse tree

    # compare the current token to each expected character
    for lexeme in grammar:

        # if they match, add the token to the tree and
        # remove it from the tokens list
        if lexeme == tokens[0][1]:
            tree.add(lexeme)
            tokens.pop(0)

        # if required is True, throw an error on mismatch
        else:
            lookup(lexeme, "error")
    return tokens, tree


def error_message(code=None):
# receives error code and calls an error with the appropriate message

    # prevent errors from missing, non-numeric, or invalid error codes
    if not code in errors.keys():
        code = 99
    raise Exception(f"Error {code}: {errors[code]}")


def lookup(expression, column=""):

    record = lookup_table.get(expression)

    if column == "error":
        error_message(record[1])
    else:
        return  Token(record[0])


def text_to_tokens(text, tokens_list=""):
# input:  plain text file (text)
# output: list of tuples in the form (TOKEN, lexeme) + (Token.EOF, "$")

    # base case: quit on empty text
    if len(text) == 0:
        tokens_list.append((Token["EOF"], "$"))
        return tokens_list

    # first pass setup because lists are mutable
    if type(tokens_list) == str:
        tokens_list = []

    # loop through all characters and divide into valid lexemes
    while len(text) > 0:

        # refresh lexeme and token
        lexeme = False
        token = False

        # skip spaces
        if text[0] in ["", " ", "\n", "\r", "\t"]:
            text = text[1:]             # reduce text
            return text_to_tokens(text, tokens_list)

        # identify 2-symbol operators
        if text[0:2] in lookup_table.keys():
            lexeme = text[0:2]

        # symbols are being finicky
        if text[0:1] in lookup_table.keys() and not lexeme:
            lexeme = text[0:1]

        # for all other characters:
        if not lexeme:
            # check keywords first
            for key in (lookup_table.keys()):

                # re escape keeps variable names from interfering with this function
                # the walrus operator := assigns the result to the variable 'match'
                if bool(match:=re.match(re.escape(key), re.escape(text))):
                    # if there is a match, set lexeme to the matching string
                    lexeme = match.group(0)
                    break

            # if there wasn't a keyword match, check regex patterns
            if not lexeme:
                for pattern in regex_patterns.items():
                     # can't escape the 'text' variable below because it will
                     # not recognize floats
                     if bool(match:=re.match(pattern[1], text)):
                        # set both lexeme and token
                        lexeme = match.group(0)
                        token = Token[pattern[0]]
                        break

        # if token is not already set, look it up now
        if bool(lexeme) and not bool(token):
            token = lookup(lexeme)

        # if bool and lexeme are both set, append to list
        if bool(lexeme):
            tokens_list.append((token, lexeme))
            # reduce text by the length of the word we just added
            text = text[len(lexeme):]

            # recursion !
            return text_to_tokens(text, tokens_list)

        # if the text matched no lexemes, throw an error
        else:
            error_message(3)


######### Parse Tree ###################################################
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


######### Productions ##################################################

def parse(text):

    # convert text to (token, lexeme) tuples
    tokens = text_to_tokens(text)

    # structure the data
    tree = Tree()

    # top level of tree is <program>
    p_program(tokens, tree)

    # return complete parse tree
    return tree


def p_program(tokens, tree):
# <program>  →  int main ( ) { <declaration>+ <statement>+ }
    tree.data = "<program>"

# TERMINALS:
    check_terminals(["int", "main", "(", ")", "{"], tokens, tree)

# < DECLARATION >  Repeat 1+ times
    p_declaration(tokens, tree)
    while tokens[0][0] in [Token.INT_TYPE, Token.BOOL_TYPE,
                           Token.CHAR_TYPE, Token.FLOAT_TYPE]:
        p_declaration(tokens, tree)

# < STATEMENT >  Repeat 1+ times
    p_statement(tokens, tree)

    # <statement> must begin with if, while, {, or an identifier
    while tokens[0][0] in [
            Token.IF, Token.WHILE, Token.OPEN_CURLY, Token.IDENTIFIER]:
        p_statement(tokens, tree)

# TERMINALS:
    check_terminals("}", tokens, tree)

# END OF FILE:
    if tokens[0][0] == Token.EOF and len(tokens) == 1:
        return tree
    else:
        lookup("$", "error")


def p_declaration(tokens, tree):
# <declaration>  →  <type> <identifier> [ [ <int_literal> ] ] { , <identifier> [ [<int_literal> ] ] } ;

    subtree = Tree()
    subtree.data = "<declaration>"

# # <TYPE>
    p_type(tokens, subtree)

# <identifier>
    p_identifier(tokens, subtree)

# [ <int literal> ]                                  Repeat 0 or 1 times
    if tokens[0][0] == Token.OPEN_BRACKET:
        check_terminals("[", tokens, subtree)
        p_int_literal(tokens, subtree)
        check_terminals("]", tokens, subtree)

# , <identifier> [ <int_literal> ]                Repeat 0 or more times
    while tokens[0][0] == Token.COMMA:
        check_terminals(",", tokens, subtree)
        p_identifier(tokens, subtree)

        # [ <int literal> ]                          Repeat 0 or 1 times
        if tokens[0][0] == Token.OPEN_BRACKET:
            check_terminals("[", tokens, subtree)
            p_int_literal(tokens, subtree)
            check_terminals("]", tokens, subtree)
# ;
    check_terminals(";", tokens, subtree)

    tree.add(subtree)

    return tokens, tree


def p_statement(tokens, tree):
# <statement>  →  <assignment> | <if> | <while> | { <statement>+ }
    subtree = Tree()
    subtree.data = "<statement>"

    # if the next token is "if", call <if>
    if tokens[0][0] == Token.IF:
        p_if(tokens, subtree)

    # if the next token is "while", call <while>
    elif tokens[0][0] == Token.WHILE:
        p_while(tokens, subtree)

    # if the next token fits an identifier, call <assignment>
    elif tokens[0][0] == Token.IDENTIFIER:
        p_assignment(tokens, subtree)

    # or if it starts with {, call another <statement>
    elif tokens[0][0] == Token.OPEN_CURLY:
        # {                                         repeats 0 or 1 times
        check_terminals("{", tokens, subtree)

        # <statement>                                   Repeats 0+ times
        while tokens[0][0] != Token.CLOSE_CURLY:
            p_statement(tokens, subtree)

        # }                                  required with opening curly
        check_terminals("}", tokens, subtree)

    else:
        error_message(19)

    tree.add(subtree)
    return tokens, tree


def p_assignment(tokens, tree):
# <assignment>  →  <identifier> [ [ <expression> ] ] = <expression> ;
    subtree = Tree()
    subtree.data = "<assignment>"

# <identifier>
    p_identifier(tokens, subtree)

# [ <expression ]                                    repeat 0 or 1 times
    if tokens[0][0] == Token.OPEN_BRACKET:
        check_terminals("[", tokens, subtree)
        p_expression(tokens, subtree)
        check_terminals("]", tokens, subtree)

# =
    check_terminals("=", tokens, subtree)

# <expression>
    p_expression(tokens, subtree)

# ;
    check_terminals(";", tokens, subtree)

    tree.add(subtree)
    return tokens, tree


def p_if (tokens, tree):
# <if>  →  if ( <expression> ) <statement> [ else <statement> ]
    subtree = Tree()
    subtree.data = "<if>"

    check_terminals(["if", "("], tokens, subtree)
    p_expression(tokens, subtree)
    check_terminals(")", tokens, subtree)

# [ else <statement>]                                Repeat 0 or 1 times
    if tokens[0][0] == Token.ELSE:
        check_terminals("else", tokens, subtree)
        p_statement(tokens, subtree)

    tree.add(subtree)
    return tokens, tree


def p_while (tokens, tree):
# <while>  →  while ( <expression> ) <statement>
    subtree = Tree()
    subtree.data = "<while>"

# while (
    check_terminals(["while", "("], tokens, subtree)

# <expression>
    p_expression(tokens, subtree)

# )
    check_terminals(")", tokens, subtree)

# <statement>
    p_statement(tokens, subtree)

    tree.add(subtree)
    return tokens, tree


def p_expression (tokens, tree):
# <expression>  →  <conjunction> { || <conjunction> }
    subtree = Tree()
    subtree.data = "<expression>"

# <conjunction>
    p_conjunction(tokens, subtree)

# || <conjunction>                                       Repeat 0+ times
    while tokens[0][1] == Token.OR:
        check_terminals("||", tokens, subtree)
        p_conjunction(tokens, subtree)

    tree.add(subtree)
    return tokens, tree


def p_conjunction (tokens, tree):
# <conjunction>  →  <equality>  { && <equality> }
    subtree = Tree()
    subtree.data = "<conjunction>"

# <equality>
    p_equality(tokens, subtree)

# && <equality>                                          Repeat 0+ times
    while tokens[0][0] == Token.AND:
        check_terminals("&&", tokens, subtree)
        p_equality(tokens, subtree)

    tree.add(subtree)
    return tokens, tree


def p_equality (tokens, tree):
# <equality>  →  <relation> [ <eq_neq_op> <relation> ]
    subtree = Tree()
    subtree.data = "<equality>"

# <relation>
    p_relation(tokens, subtree)

# <eq_neq_op> <relation>                             Repeat 0 or 1 times
    if tokens[0][0] in (Token.EQUALITY, Token.INEQUALITY):
        p_eq_neq_op(tokens, subtree)
        p_relation(tokens, subtree)

    tree.add(subtree)
    return tokens, tree


def p_eq_neq_op (tokens, tree):
# <eq_neq_op>  →  == | !=
    subtree = Tree()
    subtree.data = "<eq_neg_op>"

    if tokens[0][1] in ["==", "!="]:
        subtree.add(tokens[0][1])
        tokens.pop(0)

    tree.add(subtree)
    return tokens, tree


def p_relation (tokens, tree):
# <relation>  →  <addition> [ <rel_op> <addition> ]
    subtree = Tree()
    subtree.data = "<relation>"

# <addition>
    p_addition(tokens, subtree)

# <rel_op> <addition>                                Repeat 0 or 1 times
    if tokens[0][1] in ["<", "<=", ">", ">="]:
        p_rel_op(tokens, subtree)
        p_addition(tokens, subtree)

    tree.add(subtree)
    return tokens, tree


def p_rel_op (tokens, tree):
# <rel_op>  →  < | <= | > | >=
    subtree = Tree()
    subtree.data = "<rel_op>"


    if tokens[0][1] in ["<", "<=", ">", ">="]:
        subtree.add(tokens[0][1])
        tokens.pop(0)

    tree.add(subtree)
    return tokens, tree


def p_addition (tokens, tree):
# <addition>  →  <term> { <add_sub_op> <term> }
    subtree = Tree()
    subtree.data = "<addition>"

# <term>
    p_term(tokens, subtree)

# <add_sub_op>  <term>                                   Repeat 0+ times
    while tokens[0][1] in ["+", "-"]:
        p_add_sub_op(tokens, subtree)
        p_term(tokens, subtree)

    tree.add(subtree)
    return tokens, tree


def p_add_sub_op (tokens, tree):
# <add_sub_op>  →  + | -
    subtree = Tree()
    subtree.data = "<add_sub_op>"

    if tokens[0][1] in ["+", "-"]:
        subtree.add(tokens[0][1])
        tokens.pop(0)

    tree.add(subtree)
    return tokens, tree


def p_term (tokens, tree):
# <term>  →  <factor> { <mul_div_op> <factor> }
    subtree = Tree()
    subtree.data = "<term>"

# <factor>
    p_factor(tokens, subtree)

# <mul_div_op> <factor>                                  Repeat 0+ times
    while tokens[0][0] in [Token.MULTIPLY, Token.DIVIDE]:
        p_mul_div_op(tokens, subtree)
        p_factor(tokens, subtree)

    tree.add(subtree)
    return tokens, tree


def p_mul_div_op (tokens, tree):
# <mul_div_op>  →  * | /
    subtree = Tree()
    subtree.data = "<mul_div_op>"

    if tokens[0][0] in [Token.MULTIPLY, Token.DIVIDE]:
        subtree.add(tokens[0][1])
        tokens.pop(0)

    tree.add(subtree)
    return tokens, tree


def p_factor (tokens, tree):
# <factor>  →  <identifier> [ [ <expression> ] ] | <literal> | ( <expression> )
    subtree = Tree()
    subtree.data = "<factor>"

    if tokens[0][0] == Token.IDENTIFIER:
# OR <identifier>
        p_identifier(tokens, subtree)

    # [ expression ]                                    eat 0 or 1 times
        if tokens[0][0] == Token.OPEN_BRACKET:
            check_terminals("[", tokens, subtree)
            p_expression(tokens, subtree)
            check_terminals("]", tokens, subtree)

# OR <literal>
    elif tokens[0][0] in [Token.INT_LITERAL, Token.TRUE, Token.FALSE,
                          Token.FLOAT_LITERAL, Token.CHAR_LITERAL]:
        p_literal(tokens, subtree)

# OR <expression>
    elif tokens[0][0] == Token.OPEN_PAR:
        check_terminals("(", tokens, subtree)
        p_expression(tokens, subtree)
        check_terminals(")", tokens, subtree)

    else:
        error_message()

    tree.add(subtree)
    return tokens, tree


def p_type (tokens, tree):
# <type>  →  int | bool | float | char
    subtree = Tree()
    subtree.data = "<type>"

    # remove first item from list and check if it's int, bool, char, or float
    token = tokens.pop(0)
    if token[0] in (Token.INT_TYPE, Token.BOOL_TYPE,
                    Token.CHAR_TYPE, Token.FLOAT_TYPE):
        subtree.add(token[1])
        tree.add(subtree)
    else:
        error_message(23)

    return tokens, tree


def p_identifier (tokens, tree):
# <identifier>  →  <letter> { <letter> | <digit> }

    subtree = Tree()
    subtree.data = "<identifier>"

    if tokens[0][0] == Token.IDENTIFIER:

        # for each character, call <letter> or <digit> and pass the character
        for character in tokens[0][1]:
            if character.isalpha():
                p_letter(character, subtree)
            else:
                p_digit(character, subtree)
        tokens.pop(0)

    else:
        error_message(16)

    tree.add(subtree)
    return tokens, tree


def p_letter (letter, tree):
# <letter>  →  a | b | … | z | A | B | … | Z
    subtree = Tree()
    subtree.data = "<letter>"
    if letter.isalpha():
        subtree.add(letter)
    tree.add(subtree)
    return tree


def p_digit (digit, tree):
# <digit>  →  0 | 1 | … | 9
    subtree = Tree()
    subtree.data = "<digit>"

    if digit.isnumeric():
        subtree.add(digit)
    tree.add(subtree)

    return tree


def p_literal (tokens, tree):
# <literal>  →  <int_literal> | <bool_literal> | <float_literal> | <char_literal>
    subtree = Tree()
    subtree.data = "<literal>"


    if tokens[0][0] == Token.INT_LITERAL:
        p_int_literal(tokens, subtree)

    elif tokens[0][0] in [Token.TRUE, Token.FALSE]:
        p_bool_literal(tokens, subtree)

    elif tokens[0][0] == Token.FLOAT_LITERAL:
        p_float_literal(tokens, subtree)

    elif tokens[0][0] == Token.CHAR_LITERAL:
        p_char_literal(tokens, subtree)

    else:
        error_message()

    tree.add(subtree)
    return tokens, tree


def p_int_literal (tokens, tree):
    # <int_literal>  →  <digit> { <digit> }
    subtree = Tree()
    subtree.data = "<int_literal>"

    if tokens[0][0] == Token.INT_LITERAL:
        literal = str(tokens[0][1])
        for n in literal:
            p_digit(n, subtree)
        tokens.pop(0)

    else:
        error_message(14)

    tree.add(subtree)
    return tokens, tree


def p_bool_literal (tokens, tree):
# <bool_literal>  →  true | false
    subtree = Tree()
    subtree.data = "<bool_literal>"

    if tokens[0][0] in [Token.TRUE, Token.FALSE]:
        subtree.add(tokens[0][1])
        tokens.pop(0)

    tree.add(subtree)
    return tokens, tree


def p_float_literal (tokens, tree):
# <float_literal>  →  <int_literal> . <int_literal>
    subtree = Tree()
    subtree.data = "<float_literal>"

    if tokens[0][0] == Token.FLOAT_LITERAL:

        # split float at the decimal
        float = str(tokens[0][1]).split(".")

        p_digit(float[0], subtree)
        subtree.add(".")
        p_digit(float[1], subtree)

        tokens.pop(0)

    tree.add(subtree)
    return tokens, tree


def p_char_literal (tokens, tree):
# <char_literal>  →  ' <letter> '
    subtree = Tree()
    subtree.data = "<char_literal>"

    if tokens[0][0] == Token.CHAR_LITERAL:

        character = str(tokens[0][1])

        if character[0] == character[2] == "\'":
            subtree.add("\'")
            p_letter(character[1], subtree)
            subtree.add("\'")
        else:
            lookup("'", "error")
        tokens.pop(0)

    tree.add(subtree)
    return tokens, tree

######### Main #########################################################
if __name__ == "__main__":

    # # Check for source file
    if len(sys.argv) != 2:
        error_message(1)

    source = open(sys.argv[1], "rt")
    if not source:
        error_message(2)

    file_contents = source.read()
    source.close()#


    tree = parse(file_contents)
    if tree:
        print("Input syntactically correct! Parse tree displayed.")
    tree.print()