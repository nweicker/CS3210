def parse(text):

    # split the text into lexemes
    lexemes = get_lexemes(text)

    # create the parse tree
    tree = Tree()

    # top-level grammar procedure is <program>
    p_program(lexemes, tree)

    # return the parse tree
    return tree