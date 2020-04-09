from Program1.parser import *

def check_terminals(grammar, tokens, tree):
# grammar: list of expected characters
# tokens, tree: the current state of the parse tree

    # compare the current token to each expected character
    for lexeme in grammar:
        print(lexeme)

        # if they match, add the token to the tree and
        # remove it from the tokens list
        if lexeme == tokens[0][1]:
            tree.add(lexeme)
            tokens.pop(0)

        # if required is True, throw an error on mismatch
        else:
            lookup(lexeme, "error")
    return tokens, tree


def parse(text):

# TODO
# needs integration with lexical analyzer
    # convert text to tokens
    # tokens = text_to_tokens(text)
    tokens = text

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
    if tokens[0][0] == Token.CLOSE_CURLY:
        tree.add("}")
        tokens.pop(0)
    else:
        lookup("}", "error")

# END OF FILE:
    if tokens[0][0] == Token.EOF:
        tokens.pop(0)
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

# [ <int literal> ]     Repeat 0 or 1 times
    if tokens[0][0] == Token.OPEN_BRACKET:
        check_terminals("[", tokens, subtree)
        p_int_literal(tokens, subtree)
        check_terminals("]", tokens, subtree)

# , <identifier> [ <int_literal> ]     Repeat 0 or more times
    while tokens[0][0] == Token.COMMA:
        check_terminals(",", tokens, subtree)
        p_identifier(tokens, subtree)

        # [ <int literal> ]     Repeat 0 or 1 times
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

    if tokens[0][0] == Token.IF:
        p_if(tokens, subtree)

    elif tokens[0][0] == Token.WHILE:
        p_while(tokens, subtree)

    # if the next token fits an identifier
    elif tokens[0][0] == Token.IDENTIFIER:
        p_assignment(tokens, subtree)

    elif tokens[0][0] == Token.OPEN_CURLY:
        # { statement } repeats 0+ times
        while tokens[0][0] == Token.OPEN_CURLY:
            p_statement(tokens, subtree)

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

# [ <expression ]   repeat 0 or 1 times
    if tokens[0][0] == Token.OPEN_BRACKET:
        check_terminals("[")
        p_expression(tokens, subtree)
        check_terminals("]")

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

    check_terminals("if", "(")
    p_expression(tokens, subtree)
    check_terminals(")")

# [ else <statement>]     Repeat 0 or 1 times
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
    check_terminals("(", tokens, subtree)

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

# || <conjunction>  Repeat 0+ times
    while tokens[0][1] == Token.OR:
        check_terminals("||", tokens, subtree)
        p_conjunction(tokens, subtree)

    tree.add(subtree)
    return tokens, tree


def p_conjunction (tokens, tree):
# <conjunction>  →  <equality> { && <equality> }
    subtree = Tree()
    subtree.data = "<conjunction>"

# <equality>
    p_equality(tokens, subtree)
# && <equality>  Repeat 0+ times
    while tokens[0][0] == Token.EQUALITY:
        check_terminals("==", tokens, subtree)
        p_equality(tokens, subtree)

    tree.add(subtree)
    return tokens, tree


def p_equality (tokens, tree):
# <equality>  →  <relation> [ <eq_neq_op> <relation> ]
    subtree = Tree()
    subtree.data = "<equality>"

# <relation>
    p_relation(tokens, subtree)

# <eq_neq_op> <relation>  Repeat 0 or 1 times
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

# <rel_op> <addition>   Repeat 0 or 1 times
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

# <add_sub_op>  <term>  Repeat 0+ times
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

# <mul_div_op> <factor>     Repeat 0+ times
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

    # [ expression ]        Repeat 0 or 1 times
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

    return tokens, tree


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

        #split float at the decimal
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

        check_terminals("\'", tokens, subtree)
        p_letter(tokens, subtree)
        check_terminals("\'", tokens, subtree)

        tokens.pop(0)

    tree.add(subtree)
    return tokens, tree


##############################################################################
path = "test_files/source 1 output.txt"

source = open(path)
file_contents = source.read()
source.close()

tokens = [  (Token.INT_TYPE, 'int'), (Token.MAIN, "main"),
            (Token.OPEN_PAR, '('), (Token.CLOSE_PAR, ')'),
            (Token.OPEN_CURLY, '{'), (Token.INT_TYPE, 'int'),
            (Token.IDENTIFIER, 'abc'), (Token.COMMA, ','),
            (Token.IDENTIFIER, 'b5e'), (Token.COMMA, ','),
            (Token.IDENTIFIER, 'c'), (Token.SEMICOLON, ';'),
            (Token.IDENTIFIER, 'abc'), (Token.ASSIGNMENT, '='),


            (Token.SEMICOLON, ';'),
            (Token.IDENTIFIER, 'b5e'), (Token.ASSIGNMENT, '='),
            (Token.INT_LITERAL, '3'), (Token.SEMICOLON, ';'),
            (Token.IDENTIFIER, 'c'), (Token.ASSIGNMENT, '='),
            (Token.IDENTIFIER, 'abc'), (Token.ADD, '+'),
            (Token.IDENTIFIER, 'b5e'), (Token.SEMICOLON, ';'),
            (Token.CLOSE_CURLY, '}'), (Token.EOF, '$')]
