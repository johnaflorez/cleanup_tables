class CleanUPTableConstants:
    """
    Class with the constants from the CleanUPTablesManager module
    """

    FULL_FORMAT_DATE = '%F %T.%f'
    LIMIT_TO_CLEAN = 50000
    SQL_NAME = 'sql/cleanup_process.sql'


class CleanUPTableHelpTextModel:
    """
    Class to manage the messages in the help text for CleanUPTables model fields.
    """

    TABLE_NAME = "This name must be included in the settings.VALID_MODELS_TO_CLEAN_UP variable before to be saved."
    DATE_FIELD = "This field must be of date type and belong to the table defined above."
    CLEAN_UP_RULE = """
        This rule must be defined in the following structure:
        <br>&emsp;- 1_day, 5_days
        <br>&emsp;- 1_week, 10_weeks
        <br>&emsp;- 1_month, 3_months
        <br>&emsp;- 1_year, 2_years
    """
    PRIORITY = "This value can be used to define the periodicity with which certain tables are cleaned."
