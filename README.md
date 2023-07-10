Cleanup Table
===============
Application to remove records from django models


Installation:
-------------
Add this new requirement:

    pip install -e git+https://github.com/johnaflorez/cleanup_tables.git@1.0.4#egg=cleanup_tables


Settings configuration:
---------
List of models name to be included in the cleanup process:

    VALID_MODELS_TO_CLEAN_UP = ['ModelName', ]

Username by default for automatic process:

    USERNAME_BY_DEFAULT = 'admin'

Add this in the INSTALLED_APPS:

    INSTALLED_APPS = (
        # ...
        'cleanup_tables',
        # ...
    )

Migration:
-----------
Django 1.2:

    python manage.py schemamigration cleanup_tables --auto
    python manage.py migrate cleanup_tables

Django >=1.11:

    python manage.py makemigrations
    python manage.py migrate


HOW TO USE:
-----------
* Register the table in the ``CleanUPTables`` model via admin.
  * ``table_name``: This name must be included in the settings.VALID_MODELS_TO_CLEAN_UP variable before to be saved.
  * ``date_field``: This field must be of date type and belong to the table defined above.
  * ``clean_up_rule``: This rule must be defined in the following structure:
        <br>&emsp;- 1_day, 5_days
        <br>&emsp;- 1_week, 10_weeks
        <br>&emsp;- 1_month, 3_months
        <br>&emsp;- 1_year, 2_years
  * ``sql_file``: (Optional) This field can be filled in case the default SQL code changes too much for what is needed in this configuration.
  * ``priority``: This value can be used to define the periodicity with which certain tables are cleaned.

* Import ``CleanUPTablesManager`` class and called the ``cleanup`` method.
* All the tables saved in the ``CleanUPTables`` model will be cleaned according to the ``clean_up_rule`` defined.


Basic example
-------------
```
>>> from cleanup_tables.models import CleanUPTables
>>> instance = CleanUPTables()
>>> instance.table_name = 'ParserFile'
>>> instance.date_field = 'created_at'
>>> instance.clean_up_rule = '6_months'
>>> instance.priority = 'normal'
>>> instance.save()


>>> from parse.utils import CleanUPTablesManager
>>> manager = CleanUPTablesManager()
>>> manager.cleanup()
>>> manager.logs_deleted
18256
```


SQL FILE
--------
This is the SQL file configured by default:
```
DELETE
  FROM {db_table_name}
  WHERE {primary_key_name} IN (
    SELECT
    {primary_key_name}
    FROM {db_table_name}
    WHERE {db_condition}
    ORDER BY
      {primary_key_name} DESC
    OFFSET 0 ROWS
    FETCH NEXT {limit} ROWS ONLY)
```

Each table saved in the ``CleanUPTables`` model can manage its own SQL file as long as it follows the established conventions:
* ``db_table_name``
* ``primary_key_name``
* ``db_condition``
* ``limit``
