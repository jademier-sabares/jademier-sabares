# PROPOSITIONAL LOGIC TRUTH TABLE GENERATOR
# GROUP 3 | Python | Dashes border | Secret feature: live character count

from itertools import product

TEAM = "Sabares, Cliff Ivan, Facturan"     # <-- team names (shown on screen)
LINE = "-" * 60                            # <-- dash border


def live_input(prompt):
    """Ask for the formula and show the character count while typing."""
    try:
        import msvcrt                       # works on Windows
    except ImportError:
        text = input(prompt)                # other computers: show count after Enter
        print("   [Characters: " + str(len(text)) + "]")
        return text

    text = ""
    print(prompt + "   [Characters: 0]" + "\b" * 17, end="", flush=True)
    while True:
        key = msvcrt.getwch()               # read one key
        if key == "\r":                     # Enter = done
            break
        if key == "\b":                     # Backspace = delete last letter
            text = text[:-1]
        elif key.isprintable():
            text = text + key
        # clear the line, then rewrite it with the new count
        count = "   [Characters: " + str(len(text)) + "]"
        print("\b" * 80 + " " * 80 + "\b" * 80, end="")
        print(prompt + text + count + "\b" * len(count), end="", flush=True)
    print()
    return text


def to_python(formula):
    """Turn our symbols into Python words so Python can calculate it."""
    return formula.replace("&", " and ").replace("|", " or ").replace("~", " not ")


def calculate(formula, values):
    """Return 1 or 0 for a formula, given values like {'P': 1, 'Q': 0}."""
    return int(eval(to_python(formula), {}, values))


def find_steps(formula):
    """Find the smaller parts: every (...) group and every ~P / ~Q / ~R."""
    parts = []
    starts = []
    for i, ch in enumerate(formula):
        if ch == "(":
            starts.append(i)
        elif ch == ")":
            s = starts.pop()
            if s > 0 and formula[s - 1] == "~":     # keep the ~ in front of ( )
                s = s - 1
            parts.append((i, formula[s:i + 1]))
        elif ch == "~" and i + 1 < len(formula) and formula[i + 1] in "PQR":
            parts.append((i + 1, formula[i:i + 2]))
    parts.sort()                                    # smallest steps first
    steps = []
    for end, text in parts:
        if text not in steps and text != formula:
            steps.append(text)
    return steps


# ---------------- START OF PROGRAM ----------------
print(LINE)
print("PROPOSITIONAL LOGIC TRUTH TABLE GENERATOR".center(60))
print("GROUP 3".center(60))
print(TEAM.center(60))
print(LINE)
print("Use P, Q, R and the symbols:  &  (AND)   |  (OR)   ~  (NOT)")
print("Example: (P & ~Q) | (P & Q)      Type 'exit' to quit.")
print(LINE)

while True:
    typed = live_input("\nEnter expression: ")
    if typed.strip().lower() == "exit":
        print("Goodbye!")
        break

    # clean up the formula: words -> symbols, no spaces, capital letters
    formula = typed.upper().replace("AND", "&").replace("OR", "|").replace("NOT", "~")
    formula = formula.replace(" ", "")

    # check that only allowed characters were used
    bad = [c for c in formula if c not in "PQR&|~()"]
    if formula == "" or bad:
        print("Error: use only P, Q, R, &, |, ~ and parentheses.")
        continue

    # make it look nice: spaces around & and |
    formula = formula.replace("&", " & ").replace("|", " | ")

    # find the variables that were used
    variables = [v for v in "PQR" if v in formula]

    # test the formula once so we can catch mistakes like "P &"
    try:
        calculate(formula, {v: 1 for v in variables})
    except Exception:
        print("Error: the formula is not written correctly.")
        continue

    steps = find_steps(formula)
    columns = variables + steps + ["FINAL OUTPUT"]

    print("\n[COMPUTING TRUTH VALUES...]")
    print("Formula length: " + str(len(typed)) + " characters")

    # header of the table
    header = "|"
    for name in columns:
        header = header + " " + name + " |"
    print("\n" + "-" * len(header))
    print(header)
    print("-" * len(header))

    # one row for every combination of 1s and 0s (starting at all 1s)
    finals = []
    for combo in product([1, 0], repeat=len(variables)):
        values = dict(zip(variables, combo))
        row = "|"
        for name in columns:
            if name == "FINAL OUTPUT":
                answer = calculate(formula, values)
                finals.append(answer)
            elif name in variables:
                answer = values[name]
            else:
                answer = calculate(name, values)
            row = row + " " + str(answer).center(len(name)) + " |"
        print(row)
    print("-" * len(header))

    print("\nVariables detected: " + str(len(variables)))
    print("Total rows evaluated: " + str(len(finals)))

    print("\n[PROPOSITIONAL ANALYSIS]")
    if 0 not in finals:
        print("The final column contains only 1s.")
        print("State: Tautology")
    elif 1 not in finals:
        print("The final column contains only 0s.")
        print("State: Contradiction")
    else:
        print("The final column contains a mix of 1s and 0s.")
        print("State: Contingent Matrix")
    print(LINE)
    print(("Group 3 | " + TEAM).center(60))
    print(LINE)
