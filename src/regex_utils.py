def test():
    print("test")

def reg_or(*args):
    body = "|".join(args)
    return f"(?:{body})"

def reg_opt(*args):
    body = reg_seq(*args)
    return f"(?:{body})?"

def reg_seq(*args):
    body = "".join(args)
    return body

def reg_rep(arg):
    return f"(?:{arg}){{1,}}"

def reg_opt_rep(arg):
    return f"(?:{arg}){{0,}}"
