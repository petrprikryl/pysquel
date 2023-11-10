import ast


class ImportVisitor(ast.NodeVisitor):
    def __init__(self):
        self.sql_alias = None

    def visit_ImportFrom(self, node):
        if node.module == "pysquel":
            for alias in node.names:
                if alias.name == "sql":
                    self.sql_alias = alias.asname or alias.name


class SQLVisitor(ast.NodeVisitor):
    def __init__(self, sql_alias):
        self.sql_alias = sql_alias
        self.sql_statements = []

    def visit_Call(self, node):
        if (
            isinstance(node.func, ast.Name)
            and node.func.id == self.sql_alias
            and len(node.args) == 1
            and isinstance(node.args[0], ast.Str)
        ):
            self.sql_statements.append(node.args[0].s)


# TODO: parse noqa
def get_sql_statements(code) -> list[str]:
    tree = ast.parse(code)
    visitor = ImportVisitor()
    visitor.visit(tree)

    if not visitor.sql_alias:
        return []

    visitor = SQLVisitor(visitor.sql_alias)
    visitor.visit(tree)
    return visitor.sql_statements
