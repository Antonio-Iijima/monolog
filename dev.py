from rich import traceback
traceback.install(show_locals=True)

from sys import argv; 
from os import system, name as OS;

(lambda PROMPT=["",""] if "-q" in argv else ["mono> ","    > "],
        COMMENT="--",
        INIT=[
"(defun null (x) (eq x '()))",
"(defun and (x y) (? x (? y 't '()) '()))",
"(defun not (x) (? x '() 't))",
"(defun or (x y) (? x 't (? y 't '())))",
"""
(defun append (x y) 
    (cond 
        ((null x) 
            y) 
        ('t 
            (cons (car x) (append (cdr x) y)))))
""",
"""
(defun pair (x y) 
    (cond 
        ((and (null x) (null y)) 
            '())
        ((and (not (atom x)) (not (atom y))) 
            (cons 
                (list (car x) (car y)) 
                (pair (cdr x) (cdr y))))))
""",
"""
(defun assoc (x y)
    (cond
        ((eq x (caar y)) 
            (cadar y))
        ('t (assoc x (cdr y)))))
""",
"(defun is (x t) (eq (type x) t))",
"(defun islist (x) (is x (type '())))",
"(defun isint (x) (is x (type 0)))",
"(defun isfloat (x) (is x (type 0.0)))",
"(defun isstr (x) (is x (type '_)))",
"(defun map (f l) (cond ((null l) '()) ('t (cons (f (car l)) (map f (cdr l))))))"
],
        BUILTINS=[
            "c[*]r",
            "quote", "atom", "eq", "cons", "cond",
            "?",
            "list",
            "+", "-", "*", "/", "%",
            ">", ">=", "<", "<=", "==",
            "defun", 
            "type"
        ],
        get = print(f"""Welcome to the monolog interpreter{f" (prompt silenced)" if "-q" in argv else ""}""") or (lambda env, x: ([val for (var, val) in env if env and x == var] or exit(f"Error: variable {x} not found"))[0]): 
    [print([
        f"{out}\n" if out 
        else out for out in [expression.removeprefix("'") if expression.startswith("'") 
        else f"{expression} is a built-in keyword." if expression in BUILTINS 
        else PRINT(PRINT, EVAL(EVAL, ENV, READ(expression)))]
    ][0], end='') for (READ, EVAL, PRINT, ENV) in 
        [
            (
                lambda expr: [
                    preprocess(preprocess, convert(convert, expr.replace("’", "'").replace("(", " ( ").replace(")", " ) ").replace("'", " ' ").split())[0]) for (convert, preprocess) in
                    [
                        (
                            lambda convert, expr:
                                expr if expr == [] 
                                else [
                                    [convert(convert, expr[1:idx]), *convert(convert, expr[idx+1:])] for idx in
                                    [i for i, c in enumerate(expr) if c == ")" and expr[:i+1].count("(") == expr[:i+1].count(")")][:1] 
                                ][0] if expr[0] == "(" 
                                else [expr[0], *convert(convert, expr[1:])],

                            lambda preprocess, expr:
                                (
                                    [] if expr == []
                                    else [preprocess(preprocess, expr[0]), *preprocess(preprocess, expr[1:])] if isinstance(expr[0], list)
                                    else [["quote", preprocess(preprocess, expr[1])], *preprocess(preprocess, expr[2:])] if expr[0] == "'"
                                    else [
                                        [retype(expr[0]), *preprocess(preprocess, expr[1:])] for retype in [
                                            lambda expr:         
                                                (
                                                    int(expr) if expr.isdecimal()
                                                    else float(expr) if "." in expr and expr.replace(".", "", 1).isnumeric()
                                                    else expr
                                                ) if isinstance(expr, str)
                                                else expr
                                        ]
                                    ][0]
                                ) if isinstance(expr, list) else expr
                        )
                    ]
                ][0],

                lambda EVAL, ENV, expr:
                    (
                        expr if isinstance(expr, (int, float))
                        else (
                            int(expr) if expr.isdecimal()
                            else float(expr) if "." in expr and expr.replace(".", "", 1).isnumeric()
                            else get(ENV, expr)
                        ) if isinstance(expr, str)
                        else expr
                    ) if not isinstance(expr, list)
                    else (
                        [] if expr in ([], False)
                        else "t" if expr == True
                        else [cxr(cxr, expr[0][1:-1], EVAL(EVAL, ENV, expr[1])) for cxr in [lambda cxr, x, out: 
                                                                    out if not x 
                                                                    else cxr(cxr, x.removesuffix("a"), out[0]) if x.endswith("a")
                                                                    else cxr(cxr, x.removesuffix("d"), out[1:]) if x.endswith("d")
                                                                    else SyntaxError
                                                                ]][0]
                                                                if isinstance(expr[0], str) 
                                                                and expr[0].startswith("c") 
                                                                and expr[0].endswith("r") 
                                                                and set(c for c in expr[0][1:-1]).issubset({"a", "d"})
                        else [(operators[expr[0]](*(expr[1:] if expr[0] in ["quote", "cond", "?", "defun"] else [EVAL(EVAL, ENV, term) for term in expr[1:]]))) if expr[0] in operators 
                            else EVAL(EVAL, ENV, [get(ENV, expr[0])] + expr[1:])
                                for operators in [
                                            {
                                                "quote" : lambda x: x,
                                                "atom" : lambda x: not isinstance(x, list),
                                                "eq" : lambda x, y: x == y,
                                                "cons" : lambda x, y: [x] + y,
                                                "cond" : lambda *expr: [
                                                        evcond(evcond, list(expr)) for evcond in [
                                                        lambda evcond, expr: 
                                                            EVAL(EVAL, ENV, expr[0][1]) if EVAL(EVAL, ENV, expr[0][0]) 
                                                            else evcond(evcond, expr[1:])
                                                        ]
                                                    ][0],

                                                "?" : lambda x, y, z: EVAL(EVAL, ENV, y) if EVAL(EVAL, ENV, x) else EVAL(EVAL, ENV, z),

                                                "list" : lambda *elems: list(elems),

                                                "+" : lambda x, y: x + y,
                                                "-" : lambda x, y: x - y,
                                                "*" : lambda x, y: x * y,
                                                "/" : lambda x, y: x / y,
                                                "%" : lambda x, y: x % y,
                                                
                                                ">" : lambda x, y: x > y,
                                                ">=" : lambda x, y: x >= y,
                                                "<" : lambda x, y: x < y,
                                                "<=" : lambda x, y: x <= y,
                                                "==" : lambda x, y: x == y,
                                                
                                                "defun" : lambda fname, params, body: ENV.insert(0, (fname, ["label", fname, ["lambda", params, body]])),

                                                "type" : type
                                            }
                                        ]
                                    ][0]
                        ) if not isinstance(expr[0], list)
                        else (
                            EVAL(EVAL, [(expr[0][1], expr[0][2])] + ENV, [expr[0][2]] + expr[1:])
                        ) if expr[0][0] == "label"
                        else (
                            EVAL(EVAL, [(param, EVAL(EVAL, ENV, arg)) for (param, arg) in zip(expr[0][1], expr[1:])] + ENV, expr[0][2])
                        ) if expr[0][0] == "lambda"
                        else exit(f"Error: invalid syntax in {expr}"),

                lambda PRINT, expr:         
                    "" if expr is None
                    else ("t" if expr else "()") if isinstance(expr, bool)
                    else f"'{PRINT(PRINT, expr[1])}" if isinstance(expr, list) and len(expr) > 0 and expr[0] == "quote" 
                    else f"({' '.join(PRINT(PRINT, elem) for elem in expr if elem != None)})" if isinstance(expr, list) 
                    else str(expr),

                []
            )
    ] for expression in iter(
        lambda: INIT.pop() if INIT else [
            SystemExit if expr in ("exit", "quit") 
            else [
                print("\nKEYWORDS\n"),
                print("\n".join(BUILTINS)),
                print(),
                ""
            ][-1] if expr == "dev.kw"
            else [
                print("\nENVIRONMENT\n"),
                print("\n".join([f"{var:7s} :: {PRINT(PRINT, val)}" for (var, val) in ENV])),
                print(),
                ""
            ][-1] if expr == "dev.env"
            else system('cls' if OS == 'nt' else 'clear') if expr == "clear"
            else expr
            for expr in [
                build(build, "") for build in [
                    lambda build, s:
                    [(
                        build(build, input(PROMPT[0])) if s.startswith(COMMENT)
                        else s if s and s.count("(") == s.count(")") 
                        else build(build,  " ".join([s, input(PROMPT[1] if s else PROMPT[0])]))
                    ) for s in [s.strip()]][0]
                ]
            ]
        ][0],
        SystemExit) if expression
    ])()
