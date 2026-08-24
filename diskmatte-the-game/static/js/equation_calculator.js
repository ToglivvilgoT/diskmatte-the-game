// Client-side evaluator + calculator UI for "equation" answer type tasks.
// Evaluates the user's expression entirely in the browser (using BigInt, so
// there is no overflow up to the same 1000 cap used server-side for
// metadata sync) and only ever sends the final integer result to the server.
// The server never re-evaluates an expression - only compares two integers.

const MAX_FACTORIAL_N = 1000n;

class EquationError extends Error {}

function gcdBig(a, b) {
    if (a < 0n) a = -a;
    if (b < 0n) b = -b;
    while (b) {
        [a, b] = [b, a % b];
    }
    return a;
}

function makeFrac(n, d = 1n) {
    if (d === 0n) {
        throw new EquationError("Kan inte dela med noll");
    }
    if (d < 0n) {
        n = -n;
        d = -d;
    }
    const g = gcdBig(n, d) || 1n;
    return { n: n / g, d: d / g };
}

const fracAdd = (a, b) => makeFrac(a.n * b.d + b.n * a.d, a.d * b.d);
const fracSub = (a, b) => makeFrac(a.n * b.d - b.n * a.d, a.d * b.d);
const fracMul = (a, b) => makeFrac(a.n * b.n, a.d * b.d);
const fracDiv = (a, b) => makeFrac(a.n * b.d, a.d * b.n);
const fracNeg = (a) => makeFrac(-a.n, a.d);
const fracIsInt = (a) => a.d === 1n;

function tokenize(text) {
    const tokens = [];
    let i = 0;
    while (i < text.length) {
        const ch = text[i];
        if (/\s/.test(ch)) {
            i += 1;
            continue;
        }
        if (/[0-9]/.test(ch)) {
            let j = i;
            while (j < text.length && /[0-9]/.test(text[j])) j += 1;
            tokens.push({ type: "num", value: BigInt(text.slice(i, j)) });
            i = j;
            continue;
        }
        if ("+-*/^!(),".includes(ch)) {
            tokens.push({ type: ch });
            i += 1;
            continue;
        }
        if (ch === "C" || ch === "c") {
            tokens.push({ type: "C" });
            i += 1;
            continue;
        }
        throw new EquationError(`Ogiltigt tecken '${ch}' i uttrycket`);
    }
    return tokens;
}

class Parser {
    constructor(tokens) {
        this.tokens = tokens;
        this.pos = 0;
    }

    peek() {
        return this.pos < this.tokens.length ? this.tokens[this.pos] : null;
    }

    advance() {
        return this.tokens[this.pos++];
    }

    expect(type) {
        const token = this.peek();
        if (!token || token.type !== type) {
            throw new EquationError(`Förväntade '${type}'`);
        }
        this.advance();
    }

    parse() {
        const value = this.expr();
        if (this.peek() !== null) {
            throw new EquationError("Oväntat tecken i uttrycket");
        }
        return value;
    }

    expr() {
        let value = this.term();
        while (this.peek() && (this.peek().type === "+" || this.peek().type === "-")) {
            const op = this.advance().type;
            const rhs = this.term();
            value = op === "+" ? fracAdd(value, rhs) : fracSub(value, rhs);
        }
        return value;
    }

    term() {
        let value = this.power();
        while (this.peek() && (this.peek().type === "*" || this.peek().type === "/")) {
            const op = this.advance().type;
            const rhs = this.power();
            value = op === "*" ? fracMul(value, rhs) : fracDiv(value, rhs);
        }
        return value;
    }

    power() {
        const base = this.unary();
        if (this.peek() && this.peek().type === "^") {
            this.advance();
            const exponent = this.power();
            if (!fracIsInt(exponent) || exponent.n < 0n) {
                throw new EquationError("Exponenten måste vara ett positivt heltal");
            }
            let result = makeFrac(1n);
            for (let i = 0n; i < exponent.n; i += 1n) {
                result = fracMul(result, base);
            }
            return result;
        }
        return base;
    }

    unary() {
        if (this.peek() && this.peek().type === "-") {
            this.advance();
            return fracNeg(this.unary());
        }
        return this.postfix();
    }

    postfix() {
        let value = this.primary();
        while (this.peek() && this.peek().type === "!") {
            this.advance();
            value = makeFrac(factorial(value));
        }
        return value;
    }

    primary() {
        const token = this.peek();
        if (!token) {
            throw new EquationError("Oväntat slut på uttrycket");
        }
        if (token.type === "num") {
            this.advance();
            return makeFrac(token.value);
        }
        if (token.type === "(") {
            this.advance();
            const value = this.expr();
            this.expect(")");
            return value;
        }
        if (token.type === "C") {
            this.advance();
            this.expect("(");
            const n = this.expr();
            this.expect(",");
            const k = this.expr();
            this.expect(")");
            return makeFrac(binomial(n, k));
        }
        throw new EquationError("Oväntat tecken i uttrycket");
    }
}

function requireNonNegativeInt(value, label) {
    if (!fracIsInt(value) || value.n < 0n) {
        throw new EquationError(`${label} måste vara ett icke-negativt heltal`);
    }
    return value.n;
}

function factorial(value) {
    const n = requireNonNegativeInt(value, "Fakultetens tal");
    if (n > MAX_FACTORIAL_N) {
        throw new EquationError(`Talet är för stort (${n}! > ${MAX_FACTORIAL_N}!)`);
    }
    let result = 1n;
    for (let i = 2n; i <= n; i += 1n) result *= i;
    return result;
}

function binomial(nValue, kValue) {
    let n = requireNonNegativeInt(nValue, "n i C(n, k)");
    let k = requireNonNegativeInt(kValue, "k i C(n, k)");
    if (n > MAX_FACTORIAL_N) {
        throw new EquationError(`Talet är för stort (n > ${MAX_FACTORIAL_N} i C(n, k))`);
    }
    if (k > n) {
        throw new EquationError("k kan inte vara större än n i C(n, k)");
    }
    k = k < n - k ? k : n - k;
    let result = 1n;
    for (let i = 0n; i < k; i += 1n) {
        result = (result * (n - i)) / (i + 1n);
    }
    return result;
}

function evaluateExpression(text) {
    if (text.trim() === "") {
        throw new EquationError("Skriv ett uttryck");
    }
    const parser = new Parser(tokenize(text));
    const value = parser.parse();
    if (!fracIsInt(value)) {
        throw new EquationError(`Resultatet (${value.n}/${value.d}) är inte ett heltal`);
    }
    return value.n;
}

document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-equation-form]").forEach((form) => {
        const input = form.querySelector("[data-equation-input]");
        const resultField = form.querySelector("[data-equation-result]");
        const preview = form.querySelector("[data-equation-preview]");
        const submitButton = form.querySelector('button[type="submit"]');
        if (!input || !resultField || !preview) return;

        const isLocked = input.hasAttribute("readonly");

        const update = () => {
            preview.classList.remove("text-danger", "text-success");
            try {
                const value = evaluateExpression(input.value);
                resultField.value = value.toString();
                preview.textContent = `= ${value}`;
                preview.classList.add("text-success");
                if (submitButton) submitButton.disabled = false;
            } catch (e) {
                resultField.value = "";
                preview.textContent = e instanceof EquationError ? e.message : "Ogiltigt uttryck";
                preview.classList.add("text-danger");
                if (submitButton) submitButton.disabled = true;
            }
        };

        if (isLocked) {
            update();
            return;
        }

        if (submitButton) submitButton.disabled = true;
        input.addEventListener("input", update);

        const insertAtCursor = (text) => {
            const start = input.selectionStart ?? input.value.length;
            const end = input.selectionEnd ?? input.value.length;
            input.value = input.value.slice(0, start) + text + input.value.slice(end);
            const cursor = start + text.length;
            input.setSelectionRange(cursor, cursor);
            input.focus();
            update();
        };

        form.querySelectorAll("[data-key]").forEach((button) => {
            button.addEventListener("click", () => insertAtCursor(button.dataset.key));
        });

        const chooseButton = form.querySelector("[data-choose]");
        if (chooseButton) {
            chooseButton.addEventListener("click", () => insertAtCursor("C(,)"));
        }

        const backspaceButton = form.querySelector("[data-backspace]");
        if (backspaceButton) {
            backspaceButton.addEventListener("click", () => {
                const start = input.selectionStart ?? input.value.length;
                const end = input.selectionEnd ?? input.value.length;
                if (start === end && start > 0) {
                    input.value = input.value.slice(0, start - 1) + input.value.slice(start);
                    input.setSelectionRange(start - 1, start - 1);
                } else {
                    input.value = input.value.slice(0, start) + input.value.slice(end);
                    input.setSelectionRange(start, start);
                }
                input.focus();
                update();
            });
        }

        const clearButton = form.querySelector("[data-clear]");
        if (clearButton) {
            clearButton.addEventListener("click", () => {
                input.value = "";
                input.focus();
                update();
            });
        }

        update();
    });
});
