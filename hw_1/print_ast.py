import ast

import matplotlib.pyplot as plt
import networkx as nx


def read_file(filepath):
    with open(filepath) as f:
        content = f.read()
    f.close()
    return content


class GraphBuilderVisitor(ast.NodeVisitor):
    def __init__(self):
        self.stack = []
        self.graph = nx.Graph()
        self.node_name = ""
        self.node_idx = 0
        self.node_labels = {}

    def generic_visit(self, node):
        cur_idx = self.node_idx
        self.node_idx += 1

        parent_idx = None

        if self.stack:
            parent_idx = self.stack[-1]

        if len(self.node_name) > 0:
            node_name = self.node_name
            self.node_name = ""
        else:
            node_name = ""
        self.stack.append(cur_idx)

        self.graph.add_node(cur_idx)
        if parent_idx is not None:
            self.graph.add_edge(cur_idx, parent_idx)
        self.node_labels[cur_idx] = node_name

        super(self.__class__, self).generic_visit(node)

        self.stack.pop()

    def visit_FunctionDef(self, node):
        self.node_name = "func\n " + node.name
        self.generic_visit(node)

    def visit_Load(self, node):
        pass

    def visit_Store(self, node):
        pass

    def visit_Subscript(self, node):
        self.node_name = "[]"
        self.generic_visit(node)

    def visit_List(self, node):
        self.node_name = "list"
        self.generic_visit(node)

    def visit_Assign(self, node):
        self.node_name = "assign"
        self.generic_visit(node)

    def visit_Compare(self, node):
        self.node_name = "cmp"
        self.generic_visit(node)

    def visit_Add(self, node):
        self.node_name = "+"
        self.generic_visit(node)

    def visit_Sub(self, node):
        self.node_name = "-"
        self.generic_visit(node)

    def visit_Eq(self, node):
        self.node_name = "="
        self.generic_visit(node)

    def visit_Or(self, node):
        self.node_name = "or"
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        self.node_name = "boolop"
        self.generic_visit(node)

    def visit_arg(self, node):
        self.node_name = "arg " + node.arg
        self.generic_visit(node)

    def visit_Name(self, node):
        self.node_name = "var " + node.id
        self.generic_visit(node)

    def visit_Constant(self, node):
        self.node_name = f"const\n{node.value}"
        self.generic_visit(node)

    def visit_Call(self, node):
        func_name = getattr(node.func, "id", "")
        if len(func_name) == 0:
            func_name = getattr(node.func, "attr", "")
        self.node_name = "func\ncall\n" + func_name
        self.generic_visit(node)

    def visit_If(self, node):
        self.node_name = "if"
        self.generic_visit(node)

    def visit_arguments(self, node):
        self.node_name = "args"
        self.generic_visit(node)

    def visit_Attribute(self, node):
        self.node_name = "attr\n" + node.attr
        self.generic_visit(node)

    def visit_Return(self, node):
        self.node_name = "return"
        self.generic_visit(node)

    def visit_BinOp(self, node):
        self.node_name = "binop"
        self.generic_visit(node)

    def visit_UnaryOp(self, node):
        self.node_name = "unop"
        self.generic_visit(node)

    def visit_USub(self, node):
        self.node_name = "-"
        self.generic_visit(node)

    def visit_Module(self, node):
        super(self.__class__, self).generic_visit(node)

    def visit_Expr(self, node):
        super(self.__class__, self).generic_visit(node)


def draw_fib_ast():
    fib_content = read_file('fib.py')
    fib_ast = ast.parse(fib_content)
    fib_ast_visitor = GraphBuilderVisitor()
    fib_ast_visitor.visit(fib_ast)
    graph = fib_ast_visitor.graph

    # uncomment in case graphviz is not installed
    # the result won't look like a tree but it will be. uh. readable

    # df = pd.DataFrame(index=graph.nodes(), columns=graph.nodes())
    # for row, data in nx.shortest_path_length(graph):
    #     for col, dist in data.items():
    #         df.loc[row,col] = dist + 20
    #
    # df = df.fillna(df.max().max())
    #
    # pos = nx.kamada_kawai_layout(graph, dist=df.to_dict())

    pos = nx.drawing.nx_pydot.graphviz_layout(graph, prog="dot")

    plt.figure(figsize=(10, 10))
    nx.draw(graph, pos, node_size=1000, node_shape="s")
    nx.draw_networkx_labels(graph, pos, labels=fib_ast_visitor.node_labels, font_size=10)

    plt.savefig('artifacts/fib_ast.png', format='png')
    # or
    # plt.show()


draw_fib_ast()
