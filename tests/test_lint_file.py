from pathlib import Path

from pysquel.linter import lint_file

sample_dir = Path(__file__).parent

samples = [sample_dir / "sample.py"]

expected = [
    [
        ("SELECT col FROM table", []),
        (
            "SELECT * FROM table\n",
            [
                {
                    "line_no": 1,
                    "line_pos": 1,
                    "code": "AM04",
                    "description": "Query produces an unknown number of result columns.",
                    "name": "ambiguous.column_count",
                }
            ],
        ),
    ]
]


def test_lint_file():
    for i, sample in enumerate(samples):
        for e, result in enumerate(lint_file(sample)):
            assert (result.sql, result.errors) == expected[i][e]
