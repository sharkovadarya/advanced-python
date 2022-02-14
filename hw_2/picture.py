def picture(name, parameters):
    param_string = ",".join(parameters)
    return f"\\includegraphics[{param_string}]{{{name}}}\n"


def graphics_package():
    return "\\usepackage{graphicx}\n"
