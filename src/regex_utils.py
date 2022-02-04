def test():
    print("test")

def reg_or(*args):
    body = "|".join(args)
    return f"(?:{body})"

def reg_opt(arg):
    return f"(?:{arg})?"

def reg_seq(*args):
    body = "".join(args)
    return body
