from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent
from sqlfluff import lint as _lint

from pysquel.analyzer import get_sql_statements


@dataclass
class Result:
    sql: str = None
    errors: list[dict] = None


def lint(sql: str) -> Result:
    exclude_rules = ["LT12"]  # Files must end with a single trailing newline.
    # dedent: Expected only single space before...
    # removeprefix: Files must not begin with newlines or whitespace.
    sql_for_lint = dedent(sql).removeprefix("\n")
    return Result(sql_for_lint, _lint(sql_for_lint, exclude_rules=exclude_rules))


def lint_code(code: str) -> Iterator[Result]:
    for sql in get_sql_statements(code):
        yield lint(sql)


def lint_file(file_path: str | Path) -> Iterator[Result]:
    with Path(file_path).open() as f:
        return lint_code(f.read())


excluded_files = [".venv"]


def lint_path(path: str | Path) -> bool:
    if Path(path).is_dir():
        files = Path(path).rglob("*.py")
    else:
        files = [path]

    all_good = True

    for file_path in files:
        if any(excluded_file in str(file_path) for excluded_file in excluded_files):
            continue

        print(str(file_path) + ":")
        for result in lint_file(file_path):
            if result.errors:
                all_good = False
                print("-" * 80)
                print(result.sql)
                print("-" * 80)
                for item in result.errors:
                    print(item)
        print("=" * 80)

    return all_good
