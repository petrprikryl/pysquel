# PySquel

POC for linting SQL statements in Python.

Relying on [sqlfluff](https://sqlfluff.com/).

The name is inspired by Czech word `paskvil` which means `messed up`.

## Concept

Using `str` subclass called `sql` to mark all SQL statements for linting.
It causes avoidance of parsing the SQL statements from all strings.

```python
from pysquel import sql

my_sql = sql("SELECT * FROM table")

# `sql` is a just subclass of the str
>>> type(my_sql)
<class 'str'>

>>> sql("SELECT * FROM {table}").format(table="super_table")
'SELECT * FROM super_table'
```

It could be better **in the future**:
* [tagstr](https://discuss.python.org/t/allow-for-arbitrary-string-prefix-of-strings/19740)
  ```python
  sql"SELECT FROM table"
  
  sql_f"SELECT FROM {table}"
  ```
* [dedent](https://discuss.python.org/t/d-string-vs-str-dedent/35907)
  ```python
  sql_d"""
    SELECT 
    FROM table
  """

  sql_df"""
    SELECT 
    FROM {table}
  """
  ```

## Usage

```python
# tests/test_lint.py

from pysquel import sql

bad_sql = sql(
    """
  SELECT * 
FROM 
          table
""")
```

Run `pysquel .` to lint all `sql` statements in the current directory:

```
tests/test_lint.py :
--------------------------------------------------------------------------------
  SELECT * 
FROM 
          table

--------------------------------------------------------------------------------
{'line_no': 1, 'line_pos': 1, 'code': 'LT01', 'description': "Expected only single space before 'SELECT' keyword. Found '  '.", 'name': 'layout.spacing'}
{'line_no': 1, 'line_pos': 1, 'code': 'LT02', 'description': 'First line should not be indented.', 'name': 'layout.indent'}
{'line_no': 1, 'line_pos': 1, 'code': 'LT13', 'description': 'Files must not begin with newlines or whitespace.', 'name': 'layout.start_of_file'}
{'line_no': 1, 'line_pos': 3, 'code': 'AM04', 'description': 'Query produces an unknown number of result columns.', 'name': 'ambiguous.column_count'}
{'line_no': 1, 'line_pos': 11, 'code': 'LT01', 'description': 'Unnecessary trailing whitespace.', 'name': 'layout.spacing'}
{'line_no': 2, 'line_pos': 5, 'code': 'LT01', 'description': 'Unnecessary trailing whitespace.', 'name': 'layout.spacing'}
{'line_no': 3, 'line_pos': 1, 'code': 'LT02', 'description': 'Expected indent of 4 spaces.', 'name': 'layout.indent'}
================================================================================
```

## TODO
* config
* exclude rules
* exclude dirs
* noqa
* `sqlfluff` config (dialect, templating, ...)
* custom token instead of `sql`?
* lint missing `sql` prefix for potential SQL statements
