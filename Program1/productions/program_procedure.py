def p_program(lexemes, tree):
    # <program>  →  int main ( ) { <declaration>+ <statement>+ }
    tree.data = "<program>"

    # confirm that program starts with required string
    compare_text = get_lexemes("int main ( ) {","",[])
    for i in compare_text:
        if i != lexemes.pop(0):
            if i in symbols:
                error_message(symbols.get(i, 99)[1])
            else:
                error_message()

    tree.print()