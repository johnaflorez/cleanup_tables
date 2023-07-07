# -*- coding: utf-8 -*-
import logging

from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldDoesNotExist
from django.db import connection, models

from cleanup_tables.choices import CLEAN_UP_PERIOD_TIME_OPTIONS, HOUR, DAY, WEEK, MONTH, YEAR
from cleanup_tables.exceptions import DateFormatException, DateFieldTypeException
from cleanup_tables.utils import CommonUtilsMethodsMixin

logger = logging.getLogger(__name__)


class CleanUPLogsManager:
    """
    Class to manage the cleanup process
    """

    FULL_FORMAT_DATE = '%F %T.%f'
    LIMIT_TO_CLEAN = 50000
    UTILS = CommonUtilsMethodsMixin

    def __init__(self):
        """
        Create an instance with the default values.
        """

        self.configurations = settings.CLEANUP_CONFIGURATIONS
        self.sql_raw = None
        self.model_class = None
        self.period_time_rule = None
        self.date_field = None

    def cleanup(self):
        """
        Process to clean the table logs data
        """

        for configuration in self.configurations:
            self._prepare_environment(configuration)
            self._delete_in_bulk()

    def _prepare_environment(self, configuration):
        """
        Prepare environment to start delete process
        """

        self._open_sql_file(configuration['sql_name'])
        self._set_model_class(configuration['model_name'])
        self._set_date(configuration['period_time_rule'])
        self._set_date_field(configuration['date_field'])

    def _set_model_class(self, table_name):
        """
        Set model class from the name

        Args:
            table_name (String): model name definition
        """

        content_type = ContentType.objects.get(model=table_name)
        self.model_class = content_type.model_class()

    def _set_date(self, clean_up_rule):
        """
        Build date from the `period_time_rule` defined
        """

        current_date = datetime.now()
        keep_hours = False
        quantity, period_time = clean_up_rule.split('_')
        if period_time.lower() in CLEAN_UP_PERIOD_TIME_OPTIONS[HOUR]:
            keep_hours = True
            _date = current_date - relativedelta(hours=int(quantity))
        elif period_time.lower() in CLEAN_UP_PERIOD_TIME_OPTIONS[DAY]:
            _date = current_date - relativedelta(days=int(quantity))
        elif period_time.lower() in CLEAN_UP_PERIOD_TIME_OPTIONS[WEEK]:
            _date = current_date - relativedelta(weeks=int(quantity))
        elif period_time.lower() in CLEAN_UP_PERIOD_TIME_OPTIONS[MONTH]:
            _date = current_date - relativedelta(months=int(quantity))
        elif period_time.lower() in CLEAN_UP_PERIOD_TIME_OPTIONS[YEAR]:
            _date = current_date - relativedelta(years=int(quantity))
        else:
            raise DateFormatException(clean_up_rule)

        if keep_hours:
            self.period_time_rule = _date
        else:
            self.period_time_rule = datetime.combine(_date, datetime.max.time())

    def _set_date_field(self, field_name):
        """
        Check and Set the date field to use as a filter
        """

        if self._model_field_exists(field_name) and self._is_date_field(field_name):
            self.date_field = field_name
        else:
            raise DateFieldTypeException(field_name)

    def _model_field_exists(self, field_name):
        """
        Validate if the `field_name` exists in the `model`

        Args:
            field_name (String): field name to check existence in the model
        """

        try:
            self.model_class._meta.get_field(field_name)
            return True
        except FieldDoesNotExist:
            return False

    def _is_date_field(self, field_name):
        """
        Validate if the field_name is date_time/date type.
        """

        return self.model_class._meta.get_field(field_name).__class__ in [models.DateTimeField, models.DateField]

    def _open_sql_file(self, sql_name):
        """
        Get SQL content
        """

        sql_buffer = self.UTILS.file.get_string_from_file(
            path=self.UTILS.file.get_base_path(__file__),
            filename=sql_name
        )
        self.sql_raw = sql_buffer.read()

    def _get_sql(self):
        """
        Generate the SQL as string mode
        """

        return self.sql_raw.format(
            db_table_name=self._db_table_name(),
            db_condition=self._db_condition(),
            limit=self.LIMIT_TO_CLEAN,
            primary_key_name=self._db_primary_key_name()
        )

    def _delete_in_bulk(self):
        """
        Delete all the logs in bulk
        """

        try:
            sql = self._get_sql()
            self._execute_sql(sql)
        except Exception as err:
            logger.error(
                '[ERROR] cleanup_tables._delete_in_bulk: {0}'.format(err),
                exc_info=True
            )

    @staticmethod
    def _execute_sql(sql):
        """
        Execute SQL query to clean the tables
        """

        with connection.cursor() as cursor:
            cursor.execute(sql)

    def _db_table_name(self):
        """
        Get table name in the database to build the SQL
        """

        return self.model_class._meta.db_table

    def _db_primary_key_name(self):
        """
        Returns the name of the primary key field for Model in current execution locate in self.model_class.

        Returns:
            str: The name of the primary key field.

        Example:
            >>> self._db_primary_key_name() #  if self.model_class = django.contrib.sessions.models.Session
            'session_key'
        """

        return self.model_class._meta.pk.name

    def _db_condition(self):
        """
        Get WHERE condition to build the SQL
        """

        condition = "{0} <= '{1}'".format(
            self.date_field,
            self.period_time_rule.strftime(self.FULL_FORMAT_DATE)[:-3]
        )
        return condition
