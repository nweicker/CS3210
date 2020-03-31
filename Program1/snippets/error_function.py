# error code to message conversion function with optional code number
def error_message(code=""):

    # prevent errors from non-numeric error codes
    if type(code) is not int:
        code = 99

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
        99: "syntax error"
    }
    print("Error: ", errors[code])
    quit()