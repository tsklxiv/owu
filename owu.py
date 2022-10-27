"""
OwU - OwO, but someone punches his left eye.
"""

from functools import reduce

TYPES = [
    "number",     # 0: value
    "string",     # 1: value
    "list",       # 2: array
    "identifier", # 3: name
    "verb",       # 4: name/function
    "nil"         # 5: nil/null
    "eof",        # 6: eof/eol check
    "function",   # 7: name/function (same as verb but with identifier)
]

def o   (t, v): return { "t": t, "v": v }
def on  (v):    return o(0, v)
def os  (v):    return o(1, v)
def ol  (v):    return o(2, v)
def oi  (v):    return o(3, v)
def ov  (v):    return o(4, v)
def btoi(v):    return 1 if v else 0 # Boolean to plain integer

NIL   = o(5, "")
EOF   = o(6, "")
TRUE  = on(1)
FALSE = on(0)

# Procedures (aka functions)
# Straight-up copied from Norvig's lis.py (https://github.com/norvig/pytudes/blob/main/py/lis.py#L15,L21)

class Procedure(object):
    def __init__(self, parms, body, env):
        self.params, self.body, self.env = parms, body, env
    def __call__(self, *args):
        env = dict(zip(self.params, args))
        env = {**env, **self.env}
        return eval(self.body, env)

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
def enum  (x):    return ol(list(map(on, range(0, x["v"]))))
def typeof(x):    return os(TYPES[x["t"]])

## List/String-specific verbs

def head   (x): return x["v"][0]
def tail   (x): return ol(x["v"][1:])
def reverse(x): return ol(x["v"][::-1])
def length (x): return on(len(x["v"]))

# Environments
def init_env():
    return {
        "+": lambda x: reduce(plus, x),
        "-": lambda x: reduce(minus, x),
        "*": lambda x: reduce(times, x),
        "/": lambda x: reduce(divide, x),
        "%": lambda x: reduce(modulo, x),
        ">": lambda x: reduce(more, x),
        "<": lambda x: reduce(less, x),
        "=": lambda x: reduce(equal, x),
        "!": lambda x: enum(x[0]),
        "h": lambda x: head(x[0]),
        "t": lambda x: tail(x[0]),
        "|": lambda x: reverse(x[0]),
        "#": lambda x: length(x[0]),
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
    if pos >= len(code):
        print("End of code. Nothing more to parse.")
        return EOF, pos + 1
    current = code[pos]
    if numeric(current):        # Numbers
        num, pos = consume(numeric, code, pos)
        return on(int(num)), pos
    elif identifier(current):   # Identifiers
        ident, pos = consume(identifier, code, pos)
        return oi(ident), pos
    elif current == "[":        # Expressions/Lists
        pos += 1
        lst = []
        while code[pos] != ']':
            val, pos = parseVal(code, pos)
            if val != NIL:
                lst.append(val)
        return ol(lst), pos + 1
    elif code == "]":
        return os("Unexpected ]"), pos + 1
    elif current == "\"":        # Strings
        pos += 1
        s = ""
        while pos < len(code):
            if code[pos] == "\"":
                break
            s += code[pos]
            pos += 1
        # pos + 1 also to skip the remaining "
        return os(s), pos + 1
    elif current == ";":        # Comments
        while pos < len(code) and code[pos] != "\n": pos += 1
        return NIL, pos
    elif symbol(current):       # Verbs/Symbols
        # Since every verb is a symbol character, we only need to consume
        # one symbol at a time
        return ov(current), pos + 1
    elif current in WHITESPACE: # Nils
        return NIL, pos + 1
    return os("Cannot identify what I am reading. Skipping"), pos + 1

def parser(code):
    "Parse a string of tokens"
    pos = 0
    lst = []
    while pos < len(code):
        val, pos = parseVal(code, pos)
        if val == EOF: break
        lst.append(val)
    # https://stackoverflow.com/a/1157160
    lst = list(filter(lambda x: x != NIL, lst))
    return lst

# Eval

def handle_verbs(op, args, env):
    if op["v"] == "?":
        cond, true, false = args
        exp = (true if eval(cond, env) else false)
        return eval(exp, env)
    else:
        return env[op["v"]](args)

def eval(x, env=global_env):
    "Evaluate an expression in an environment"
    if x["t"] == 3:   # Variable reference
        return env[x["v"]]
    elif x["t"] == 2 and len(x["v"]) > 0: # Expressions (lists)
        op = x["v"][0]
        if op["v"] == "d":
            (_, var, exp) = x["v"]
            env[var["v"]] = eval(exp, env)
            return NIL
        elif op["v"] == "l":
            _, params, body = x["v"]
            return Procedure(params, body, env)
        elif op["t"] == 3 or op["t"] == 4:
            args = [eval(exp, env) for exp in x["v"][1:]]
            print(f"Operator: {op}, Arguments: {args}")
            return handle_verbs(op, args, env)
        else:
            return x
    else:             # Literals
        return x

# Prettyprinter

def format(o):
    "Format an object"
    if o["t"] == 2:                  # Lists
        return [format(obj) for obj in o["v"]]
    elif o["t"] == 3 or o["t"] == 4: # Identifiers/Verbs
        return f'{o["v"]}'
    elif o["t"] == 5:                # Nil
        return "NIL"
    else:                            # Numbers/Strings/Other literals
        return o["v"]

# REPL

def repl(prompt="> "):
    code = None
    print("OwU Lisp 1.0\nType `q` to quit.")
    while True:
        code = input(prompt)
        if code == "q":
            exit(0)
        parsed = parser(code)
        print(f"Parsed: {parsed}")
        for expr in parsed:
            print(format(eval(expr)))

if __name__ == "__main__":
    repl()
