"""Safe evaluator for combinatorics arithmetic expressions.

Supports +, -, *, /, ^ (power), ! (factorial), parentheses and C(n, k)
(binomial coefficient / "n choose k"). Never uses eval()/exec() on input.

Used by the sync_tasks management command to turn an "equation" style
expected_answer (e.g. "6!/3!") from a trusted metadata file into a plain
integer stored on the Task. Not used to evaluate untrusted user input -
that evaluation happens client-side in JavaScript, and the server only
ever receives the already-computed integer.
"""

from fractions import Fraction

MAX_FACTORIAL_N = 1000


class ExpressionError(ValueError):
    """Raised when an expression is malformed or does not evaluate to an integer."""


def evaluate_to_int(expression: str) -> int:
    """Evaluate a combinatorics expression and return its integer value.

    Raises ExpressionError if the expression is invalid or does not
    evaluate to an integer.
    """
    parser = _Parser(expression)
    value = parser.parse()
    if value.denominator != 1:
        raise ExpressionError(f"Resultatet ({value}) är inte ett heltal")
    return int(value)


class _Parser:
    def __init__(self, text: str):
        self._tokens = _tokenize(text)
        self._pos = 0

    def parse(self) -> Fraction:
        value = self._expr()
        if self._peek() is not None:
            raise ExpressionError(f"Oväntat tecken vid '{self._peek()}'")
        return value

    def _peek(self):
        return self._tokens[self._pos] if self._pos < len(self._tokens) else None

    def _advance(self):
        token = self._peek()
        self._pos += 1
        return token

    def _expect(self, token):
        if self._peek() != token:
            raise ExpressionError(f"Förväntade '{token}'")
        self._advance()

    def _expr(self) -> Fraction:
        value = self._term()
        while self._peek() in ("+", "-"):
            op = self._advance()
            rhs = self._term()
            value = value + rhs if op == "+" else value - rhs
        return value

    def _term(self) -> Fraction:
        value = self._power()
        while self._peek() in ("*", "/"):
            op = self._advance()
            rhs = self._power()
            if op == "*":
                value = value * rhs
            else:
                if rhs == 0:
                    raise ExpressionError("Kan inte dela med noll")
                value = value / rhs
        return value

    def _power(self) -> Fraction:
        base = self._unary()
        if self._peek() == "^":
            self._advance()
            exponent = self._power()
            if exponent.denominator != 1:
                raise ExpressionError("Exponenten måste vara ett heltal")
            exponent_int = int(exponent)
            if exponent_int < 0:
                raise ExpressionError("Exponenten måste vara ett positivt heltal")
            return Fraction(base ** exponent_int)
        return base

    def _unary(self) -> Fraction:
        if self._peek() == "-":
            self._advance()
            return -self._unary()
        return self._postfix()

    def _postfix(self) -> Fraction:
        value = self._primary()
        while self._peek() == "!":
            self._advance()
            value = Fraction(_factorial(value))
        return value

    def _primary(self) -> Fraction:
        token = self._peek()
        if token is None:
            raise ExpressionError("Oväntat slut på uttrycket")
        if isinstance(token, Fraction):
            self._advance()
            return token
        if token == "(":
            self._advance()
            value = self._expr()
            self._expect(")")
            return value
        if token == "C":
            self._advance()
            self._expect("(")
            n = self._expr()
            self._expect(",")
            k = self._expr()
            self._expect(")")
            return Fraction(_binomial(n, k))
        raise ExpressionError(f"Oväntat tecken '{token}'")


def _require_nonnegative_int(value: Fraction, label: str) -> int:
    if value.denominator != 1 or value < 0:
        raise ExpressionError(f"{label} måste vara ett icke-negativt heltal")
    return int(value)


def _factorial(value: Fraction) -> int:
    n = _require_nonnegative_int(value, "Fakultetens tal")
    if n > MAX_FACTORIAL_N:
        raise ExpressionError(f"Talet är för stort ({n}! > {MAX_FACTORIAL_N}!)")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def _binomial(n_value: Fraction, k_value: Fraction) -> int:
    n = _require_nonnegative_int(n_value, "n i C(n, k)")
    k = _require_nonnegative_int(k_value, "k i C(n, k)")
    if n > MAX_FACTORIAL_N:
        raise ExpressionError(f"Talet är för stort (n > {MAX_FACTORIAL_N} i C(n, k))")
    if k > n:
        raise ExpressionError("k kan inte vara större än n i C(n, k)")
    k = min(k, n - k)
    result = 1
    for i in range(k):
        result = result * (n - i) // (i + 1)
    return result


def _tokenize(text: str) -> list["Fraction | str"]:
    tokens: list[Fraction | str] = []
    i = 0
    length = len(text)
    while i < length:
        char = text[i]
        if char.isspace():
            i += 1
            continue
        if char.isdigit():
            j = i
            while j < length and text[j].isdigit():
                j += 1
            tokens.append(Fraction(int(text[i:j])))
            i = j
            continue
        if char in "+-*/^!(),":
            tokens.append(char)
            i += 1
            continue
        if char in "Cc":
            tokens.append("C")
            i += 1
            continue
        raise ExpressionError(f"Ogiltigt tecken '{char}' i uttrycket")
    return tokens
