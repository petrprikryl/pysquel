import sys
from pathlib import Path
from textwrap import dedent
from sqlfluff import lint as _lint

from pysquel.analyzer import get_sql_statements


def lint(sql: str):
    exclude_rules = ["LT12"]  # Files must end with a single trailing newline.
    # dedent: Expected only single space before...
    # removeprefix: Files must not begin with newlines or whitespace.
    sql_for_lint = dedent(sql).removeprefix("\n")
    return _lint(sql_for_lint, exclude_rules=exclude_rules)


def lint_code(code: str):
    for sql in get_sql_statements(code):
        yield sql, lint(sql)


def lint_file(file_path: str | Path):
    with Path(file_path).open() as f:
        return lint_code(f.read())


def lint_dir(dir_path: str | Path):
    all_good = True

    for file_path in Path(dir_path).rglob("*.py"):
        print(file_path, ":")
        for sql, result in lint_file(file_path):
            if result:
                all_good = False
                print("-" * 80)
                print(sql)
                print("-" * 80)
                for item in result:
                    print(item)
        print("=" * 80)

    return all_good


if __name__ == "__main__":
    all_good = True

    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            all_good &= lint_dir(arg)
    else:
        all_good = lint_dir(".")

    sys.exit(0 if all_good else 1)
