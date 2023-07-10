# -------------------------------------------------------------
# CleanUP Period time Options
# -------------------------------------------------------------
HOUR = 'hour'
DAY = 'day'
WEEK = 'week'
MONTH = 'month'
YEAR = 'year'

CLEAN_UP_PERIOD_TIME_OPTIONS = {
    HOUR: ['hour', 'hours'],
    DAY: ['day', 'days'],
    WEEK: ['week', 'weeks'],
    MONTH: ['month', 'months'],
    YEAR: ['year', 'years'],
}

# -------------------------------------------------------------
# CleanUP Status Options
# -------------------------------------------------------------
NEW = 'new'
SUCCESS = 'success'
ERROR = 'error'
CLEANING = 'cleaning'
CLEAN_UP_STATUS_OPTIONS = (
    (NEW, 'New'),
    (CLEANING, 'Cleaning'),
    (SUCCESS, 'Success'),
    (ERROR, 'Error'),
)

# -------------------------------------------------------------
# Clean UP Priority Options
# -------------------------------------------------------------
HIGH = 'high'
NORMAL = 'normal'
LOW = 'low'
CLEAN_UP_PRIORITY_OPTIONS = (
    (HIGH, 'High'),
    (NORMAL, 'Normal'),
    (LOW, 'Low'),
)
