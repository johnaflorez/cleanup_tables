Cleanup Table
===============
Application to remove records from django models


Installation:
-------------
Use ``pip``:

    pip install -e git+https://github.com/johnaflorez/cleanup_tables.git@1.0.1#egg=cleanup_tables


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

HOW TO USE:
-----------

