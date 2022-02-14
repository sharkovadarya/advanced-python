import os
import subprocess
import sys

from fib_ast.print_ast import draw_fib_ast
from latex import tex_with_table_and_pic


def pdf_from_tex(tex_path, output_dir):
    subprocess.run(["pdflatex", "-output-directory", output_dir, tex_path])


def create_pdf_from_arguments(args, table_values):
    if len(args) != 4:
        print("Usage: path to fib function source, fib AST picture filename, tex filename, output directory")
        return

    output_dir = args[3]

    pic_filepath = os.path.join(output_dir, args[1])
    draw_fib_ast(args[0], pic_filepath)
    tex_text = tex_with_table_and_pic(table_values, pic_filepath)
    tex_path = os.path.join(output_dir, args[2])
    with open(tex_path, "w+") as f:
        f.write(tex_text)
    pdf_from_tex(tex_path, output_dir)


# please notice that one of the arguments is the path to the fib.py
# which for this repository is '../hw_1/fib_ast/fib.py'
if __name__ == '__main__':
    # the problem statement says nothing on which table data to use
    # and this was easier than parsing a string from command line arguments
    create_pdf_from_arguments(sys.argv[1:], [["11", "12", "13"], ["21", "22", "23"], ["31", "32", "33"]])
