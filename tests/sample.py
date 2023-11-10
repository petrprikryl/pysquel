from pysquel import sql

good_sql = sql("SELECT col FROM table")

bad_sql = sql(
    """
SELECT * FROM table
"""
)
