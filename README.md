# `monolog`

##### Disclaimer: I am not responsible for any distress caused by exposure to the programming techniques contained in this code. Peruse at your own risk.

`monolog` is a Lisp-family programming language interpreter implemented in a single Python expression.

## Table of Contents

- [The Challenge](#the-challenge)
- [The Results](#the-results)
- [Nota Bene](#nota-bene)
- [License](#license)

## The Challenge

`monolog` is the result of a challenge I set myself with the following constraints:

1. The language must be at least equivalent to the implementation of Lisp found in Paul Graham's *The Roots of Lisp*.
2. The implementation can only use vanilla Python; no imports allowed.
3. The implementation must be a *single line of code*; no semicolons allowed.

There are multiple ways such a program could be implemented; `monolog` provides one such way. Neither brevity nor efficiency were considered in the making of this interpreter.

## The Results

The intrigued programmer will observe on perusing the source code that the final product, while it fulfills the first requirement, seemingly ignores the other two. This, however, is somewhat cosmetic: the two imported modules (`sys` and `os`) provide quality of life features like prompt silencing and a terminal `clear` command; they are intentionally *not* used in the main logic of the program itself, and can be excised with minimal complications.

Other than this minor qualification, `monolog` is quite successful, surpassing its initial goals. It implements everything mentioned in Graham's essay, from arbitrary `cxr`-form operators to function definition. It even includes arithmetic operations, a ternary operator `?`, metakeywords `dev.env` and `dev.kw`, and a bunch of built-in functions defined at runtime.

## Nota Bene

###### N.B. The Latin phrase *nota bene* translates to *note well*, and is often used to indicate useful further information.

The provided files include:

- `monolog.py` - the single line of code itself.
- `dev.py` - the 'developer' version of the program, since writing the whole thing on one line would be a nightmare.
- `convert.py` - a (coincidentally) single line implementation of a multiline to single line converter, specifically designed for the **current implementation** of `dev.py`. Particularly, be careful when changing the number of lines to ignore at the beginning of `dev.py` to avoid breaking the one-line version.
- `examples.txt` and `interpreter.txt` - just some sample code; the interpreter is copied verbatim from *TRoL* (a truly lamentable abbreviation).

Files may be directed to the interpreter through standard input: `python3 monolog.py -q < interpreter.py`. I **highly recommend** using the `-q` flag when reading file input to silence the interpreter prompt.

`quit` must be placed at the end of any input files to prevent an `EOFError`; to my knowledge there is no way to catch this within the constraints, but I would welcome suggestions.

I hope this silly little project of mine brings you some entertainment, or perhaps even teaches you something new about Python along the way!

## License

`monolog` is licensed under a [GNU General Public License](https://github.com/Antonio-Iijima/alvin/blob/main/LICENSE).
