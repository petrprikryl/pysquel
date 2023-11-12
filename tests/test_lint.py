from pysquel import sql
from pysquel.linter import lint

good_sql_1 = sql("SELECT col FROM table")

good_sql_2 = sql(
    """
SELECT col FROM table
"""
)

good_sql_3 = sql(
    """
    SELECT col
    FROM table
"""
)

###

# double new line at the beginning
bad_sql_1 = sql(
    """

SELECT col FROM table
"""
)

bad_sql_2 = sql(
    """
  SELECT * 
FROM 
          table
"""
)

good = [
    good_sql_1,
    good_sql_2,
    good_sql_3,
]
bad = [
    bad_sql_1,
    bad_sql_2,
]


def test_lint():
    for is_good, sql_list in [[True, good], [False, bad]]:
        for _sql in sql_list:
            result = lint(_sql)
            print(_sql)
            print("-" * 80)
            if not result.errors:
                print("OK")
            for item in result.errors:
                print(item)
            print("=" * 80)

            assert (is_good and not result.errors) or (not is_good and result.errors)
