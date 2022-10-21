"""
OwU - OwO, but someone punches his left eye.
"""

from pprint import pp

TYPES = [
    "number",     # 0: value
    "string",     # 1: value
    "list",       # 2: array
    "identifier", # 3: name
    "verb",       # 4: name/function?
    "nil"         # 5: nil/null
]
VERBS_LIST = ["+", "-", "*", "/", "%", ">", "<", "=", "|", "#", "!", "@", "$", "^", "`"]

def o   (t, v): return { "t": t, "v": v }
def on  (v):    return o(0, v)
def os  (v):    return o(1, v)
def ol  (v):    return o(2, v)
def oi  (v):    return o(3, v)
def ov  (v):    return o(4, v)
def btoi(v):    return 1 if v else 0 # Boolean to plain integer

NIL   = o(5, "")
TRUE  = on(1)
FALSE = on(0)

# Primitive verbs

def plus  (x, y): return on(x["v"] + y["v"])
def minus (x, y): return on(x["v"] - y["v"])
def times (x, y): return on(x["v"] * y["v"])
def divide(x, y): return on(x["v"] / y["v"])
def modulo(x, y): return on(x["v"] % y["v"])
def more  (x, y): return on(btoi(x["v"] > y["v"]))
def less  (x, y): return on(btoi(x["v"] < y["v"]))
def equal (x, y): return on(btoi(x["v"] == y["v"]))
def maxo  (x, y): return on(max(x["v"], y["v"]))
def mino  (x, y): return on(min(x["v"], y["v"]))
def negate(x):    return on(-x["v"])
def enum  (x):    return ol(list(range(x["v"])))
def typeof(x):    return os(TYPES[x["t"]])

## List/String-specific verbs

def first  (x): return x["v"][0]
def reverse(x): return x["v"][::-1]
def length (x): return on(len(x["v"]))

# Helper functions

def peek(x):
    if len(x) > 0: return x[-1]
    raise IndexError
def swap(x, y, z):
    x[y], x[z] = x[z], x[y]
    return x

# Environments
def init_env():
    return {
        "+": lambda x: plus(x[0], x[1]),
        "-": lambda x: minus(x[0], x[1]),
        "*": lambda x: times(x[0], x[1]),
        "/": lambda x: divide(x[0], x[1]),
        "%": lambda x: modulo(x[0], x[1]),
        ">": lambda x: more(x[0], x[1]),
        "<": lambda x: less(x[0], x[1]),
        "=": lambda x: equal(x[0], x[1]),
    }
global_env = init_env()

# Parser/Tokenizer

WHITESPACE = " \n\t\r\f"
numeric = lambda c: c.isnumeric()
identifier = lambda c: c.isalpha() and c not in WHITESPACE
symbol = lambda c: c.isascii() and c not in WHITESPACE

def consume(cond, code, pos):
    "Consume a token in `code` until the condition `cond` is false"
    prev_pos = pos
    pos += 1
    while pos < len(code) and cond(code[pos]):
        pos += 1
    return code[prev_pos:pos], pos

def parseVal(code, pos):
    "Parse each value in `code` at position `pos`"
    current = code[pos]
    if numeric(current):
        num, pos = consume(numeric, code, pos)
        return on(int(num)), pos
    elif identifier(current):
        ident, pos = consume(identifier, code, pos)
        if ident in VERBS_LIST:
            return ov(ident), pos
        return oi(ident), pos
    elif current == "[":
        pos += 1
        lst = []
        while True:
            val, pos = parseVal(code, pos)
            if val != NIL:
                lst.append(val)
            if val["v"] == "]": break
        # Here we need to pop() the list to remove the remaining ]
        lst.pop()
        return ol(lst), pos
    elif symbol(current):
        # Since every verb is a symbol character, we only need to consume
        # one symbol at a time
        return ov(current), pos + 1
    elif current in WHITESPACE:
        return NIL, pos + 1
    return os("Cannot identify what I am reading. Skipping"), pos + 1

def parser(code):
    "Parser"
    pos = 0
    lst = []
    while pos < len(code):
        val, pos = parseVal(code, pos)
        lst.append(val)
    # https://stackoverflow.com/a/1157160
    lst = list(filter(lambda x: x != NIL, lst))
    return lst

# Eval

def eval(x, env):
    "Evaluate an expression in an environment"
    if x["t"] == 3:   # Variable reference
        return env[x]
    elif x["t"] == 2: # Expressions (lists)
        op = x["v"][0]
        args = [eval(exp, env) for exp in x["v"][1:]]
        if op["t"] == 3 or op["t"] == 4:
            env[op["v"]](args)
        else:
            return x["v"]
    else:             # Literals
        return x

# Prettyprinter

def format(o):
    "Format an object"
    return o["v"]

# Main

def main():
    code = """
    10
    """
    pp(parser(code))
    pp(eval(parser(code)))

if __name__ == "__main__":
    main()
