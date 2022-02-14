def table_row(values, last_line=False):
    return " & ".join(values) + (" \\\\" if not last_line else "") + ("\n" if len(values) > 0 else "")


def table_alignment(n, alignment):
    return "{ " + " ".join([alignment] * n) + " }" if n > 0 else ""


def table(values):
    return "\\begin{tabular}" + \
           table_alignment(len(values[0]) if len(values) > 0 else 0, "c") + "\n" + \
           "".join(map(lambda p: table_row(p[1], p[0] == len(values) - 1), enumerate(values))) + \
           "\\end{tabular}\n"
