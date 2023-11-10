from pysquel.analyzer import get_sql_statements

test_sql = '''
from pysquel import sql

good_sql = sql("SELECT col FROM table")

bad_sql = sql("""
SELECT * FROM table
""")
'''


def test_get_sql_statements():
    assert get_sql_statements(test_sql) == [
        "SELECT col FROM table",
        "\nSELECT * FROM table\n",
    ]
