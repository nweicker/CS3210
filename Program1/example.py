lookupToken = {
    # lexeme to token conversion map
    "$": Token.EOF,
    "+": Token.ADDITION,
    "-": Token.SUBTRACTION,
    "*": Token.MULTIPLICATION,
    "/": Token.DIVISION
}


class Tree:
# a tree-like data structure
    TAB = "   "

    def __init__(self):
        self.data     = None
        self.children = []

    def add(self, child):
        self.children.append(child)

    def print(self, tab = ""):
        if self.data != None:
            print(tab + self.data)
            tab += self.TAB
            for child in self.children:
                if isinstance(child, Tree):
                    child.print(tab)
                else:
                    print(tab + child)

def parse(input):
#parse
    # TODOd: create the parse tree
    tree = Tree()

    # call parse expression
    parseExpression(input, tree)

    # return the parse tree
    return tree

def parseExpression(input, tree):
    # <expression>  -> <term> <expression’>
    # <expression'> -> (+|-) <term> <expression'>
    # <expression'> -> epsilon
    # TODOd: update the tree's root with the label <expression>
    tree.data = "<expression>"

    # TODOd: call parse a term
    input, lexeme, token = parseTerm(input, tree)

    # parse more terms
    while True:
        # TODOd: if current token is + or - then add the lexeme to the tree and call parse term again
        if token == Token.ADDITION or token == Token.SUBTRACTION:
            tree.add(lexeme)
            input, lexeme, token = parseTerm(input, tree)

        # TODOd: check for EOF
        elif token == Token.EOF:
            break

        # TODOd: raise an exception
        else:
            raise Exception(errorMessage(6))

    # TODO: return the parse tree
    return tree

def parseTerm(input, tree):
    # <term> -> <factor> <term’>
    # <term'> -> (*|/) <factor> <term'>
    # <term'> -> epsilon
    # TODOd: create a subtree with the label <term>
    subTree = Tree()
    subTree.data = "<term>"

    # TODOd: attach the subtree as a child of tree
    tree.add(subTree)

    # TODOd: call parse a factor
    input, lexeme, token = parseFactor(input, subTree)

    # parse more factors
    while True:
        # TODOd: if current token is * or / then add the lexeme to the tree and call parse factor again
        if token == Token.MULTIPLICATION or token == Token.DIVISION:
            subTree.add(lexeme)
            input, lexeme, token = parseFactor(input, subTree)

        # TODOd: anything different than * or / then break the loop
        else:
            break

    # TODOd: return input, lexeme, token
    return input, lexeme, token

def parseFactor(input, tree):
    # <factor> -> <identifier> | <literal>
    # TODOd: create a subtree with the label <factor>
    subTree = Tree()
    subTree.data = "<factor>"

    # TODOd: attach the subtree as a child of tree
    tree.add(subTree)

    # TODOd: read a token
    input, lexeme, token = lex(input)

    # TODOd: if token is an identifier or literal, add the lexeme as child of subTree and read the next token
    if token == Token.IDENTIFIER or token == Token.LITERAL:
        subTree.add(lexeme)
        input, lexeme, token = lex(input)

    # TODOd: anything different than identifier or literal, raise an exception
    else:
        raise Exception(errorMessage(11))

    # TODOd: return input, lexeme, token
    return input, lexeme, token


def getChar(input):
# reads the next char from input and returns its class
    if len(input) == 0:
        return (None, CharClass.EOF)
    c = input[0].lower()
    if c.isalpha():
        return (c, CharClass.LETTER)
    if c.isdigit():
        return (c, CharClass.DIGIT)
    if c == '"':
        return (c, CharClass.QUOTE)
    if c in ['+', '-', '*', '/']:
        return (c, CharClass.OPERATOR)
    if c in ['.', ';']:
        return (c, CharClass.PUNCTUATOR)
    if c in [' ', '\n', '\t']:
        return (c, CharClass.BLANK)
    if c in ['(', ')']:
        return (c, CharClass.DELIMITER)
    return (c, CharClass.OTHER)

def getNonBlank(input):
# calls getChar and addChar until it returns a non-blank
    ignore = ""
    while True:
        c, charClass = getChar(input)
        if charClass == CharClass.BLANK:
            input, ignore = addChar(input, ignore)
        else:
            return input

def addChar(input, lexeme):
# adds the next char from input to lexeme, advancing the input by one char
    if len(input) > 0:
        lexeme += input[0]
        input = input[1:]
    return (input, lexeme)

def lex(input):
# returns the next (lexeme, token) pair or ("", EOF) if EOF is reached
    input = getNonBlank(input)

    c, charClass = getChar(input)
    lexeme = ""

    # checks EOF
    if charClass == CharClass.EOF:
        return (input, lexeme, Token.EOF)

    # reads an identifier
    if charClass == CharClass.LETTER:
        input, lexeme = addChar(input, lexeme)
        while True:
            c, charClass = getChar(input)
            if charClass == CharClass.LETTER or charClass == CharClass.DIGIT:
                input, lexeme = addChar(input, lexeme)
            else:
                return (input, lexeme, Token.IDENTIFIER)

    # reads digits
    if charClass == CharClass.DIGIT:
        input, lexeme = addChar(input, lexeme)
        while True:
            c, charClass = getChar(input)
            if charClass == CharClass.DIGIT:
                input, lexeme = addChar(input, lexeme)
            else:
                return (input, lexeme, Token.LITERAL)

    # reads operator
    if charClass == CharClass.OPERATOR:
        input, lexeme = addChar(input, lexeme)
        if lexeme in lookupToken:
            return (input, lexeme, lookupToken[lexeme])

    # TODOd: read open/close parenthesis
    if charClass == CharClass.DELIMITER:
        if c == '(' or c == ')':
            input, lexeme = addChar(input, lexeme)
            return (input, lexeme, lookupToken[lexeme])

    # anything else, raises an error
    raise Exception(errorMessage(3))








# MAIN PROGRAM ----------------------------------------------------

# checks if source file was passed and if it exists
if len(sys.argv) != 2:
    raise ValueError("Missing source file")
source = open(sys.argv[1], "rt")
if not source:
    raise IOError("Couldn't open source file")
input = source.read()
source.close()
output = []

# makes a tree class object, returns that object
tree = parse(input)

# prints the tree if the code is syntactically correct
if tree:
    print("Input is syntactically correct!")
    print("Parse Tree:")
    tree.print()
else:
    # prints error message otherwise
    print("Code has syntax errors!")
