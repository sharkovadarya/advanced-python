from hw_2.table import table
from hw_2.picture import picture, graphics_package


def document(doc_class, packages, content):
    return f"\\documentclass{{{doc_class}}}\n" + packages + "\\begin{document}\n" + content + "\\end{document}"


def tex_with_table_and_pic(table_values, pic):
    packages = graphics_package()

    table_content = table(table_values)
    image_content = picture(pic, ["width=\\linewidth"])
    content = table_content + image_content
    return document("article", packages, content)
