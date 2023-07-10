import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db import connection, transaction

from cleanup_tables.choices import CLEANING, ERROR, SUCCESS
from cleanup_tables.constants import CleanUPTableConstants
from cleanup_tables.models import CleanUPTables
from cleanup_tables.utils import CommonUtilsMethodsMixin


class CleanUPTablesManager(CleanUPTableConstants, CommonUtilsMethodsMixin):
    """
    Class to manage the cleanup process
    """

    def __init__(self, instance_id=None, priority=None, user_id=None):
        """
        Create an instance with the default values.
        Args:
            instance_id (integer, optional): A CleanUPTable instance ID
            priority (string, optional): high/medium/low
            user_id (int, optional): ID of the user who launch the process
        """

        self.instance_id = instance_id
        self.priority = priority
        self.user_id = user_id
        self._sql = None
        self.sql_raw = None
        self.model_class = None
        self.date_rule = None
        self.errors = None
        self.user = None
        self.logs_deleted = 0
        self.total_events = 0

    def cleanup(self):
        """
        Process to clean the table logs data
        """

        tables = self._get_tables_to_clean()
        for table in tables:
            table = self._prepare_environment(table)
            self._delete_in_bulk()
            self._finish_instance(table)

    def _get_tables_to_clean(self):
        """
        Get CleanUPTable queryset
        """

        params = {
            'active': True
        }
        if self.instance_id:
            params.update({'id': self.instance_id})
        elif self.priority:
            params.update({'priority': self.priority})
        return CleanUPTables.objects.filter(**params)

    def _prepare_environment(self, table):
        """
        Prepare environment to start delete process
        """

        self._initiate_variables(table)
        self.model_class = table.get_model_class(table.table_name)
        self.date_rule = table.get_date()
        self.date_field = table.date_field
        self.total_events = self._total_data_to_delete()
        self.sql_raw = self._open_sql_file(table.sql_file)
        self.user = self._get_user()
        return table

    def _initiate_variables(self, table):
        """
        Set 'cleaning' status to the table instance.
        Initialize `error` and `logs_deleted` variables.
        """

        self.errors = None
        self.model_class = None
        self.date_rule = None
        self.logs_deleted = 0
        self.total_events = 0
        table.status = CLEANING
        table.errors = None
        table.save()
        return table

    def _total_data_to_delete(self):
        """
        Get from model the total data to delete during the process and define the number of times the sql
        will be called according to the limit allowed in the CleanUPTableConstants.LIMIT_TO_CLEAN constant
        """

        date_field = '{0}__lte'.format(self.date_field)
        total_data = self.model_class.objects.filter(**{date_field: self.date_rule}).count()
        if total_data:
            return int(round((total_data / self.LIMIT_TO_CLEAN), 0)) + 1
        return 0

    def _get_user(self):
        """
        Ger User instance
        """

        if self.user_id:
            params = {'id': self.user_id}
        else:
            params = {'username': settings.USERNAME_BY_DEFAULT}
        return User.objects.get(**params)

    def _open_sql_file(self, sql_file):
        """
        Get SQL content
        """

        if sql_file:
            path = sql_file.path
        else:
            path = os.path.join(self.file.get_base_path(__file__), self.SQL_NAME)

        return self.file.get_string_from_file(path=path)

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
            for _ in range(self.total_events):
                self._execute_sql(sql)
                self._manage_transaction()
        except Exception as err:
            self._manage_transaction(transaction_type='rollback')
            self.errors = '{0}'.format(err)

    def _execute_sql(self, sql):
        """
        Execute SQL query to clean the tables
        """

        with connection.cursor() as cursor:
            cursor.execute(sql)
            self.logs_deleted += cursor.rowcount

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
            self.date_rule.strftime(self.FULL_FORMAT_DATE)[:-3]
        )
        return condition

    @staticmethod
    def _manage_transaction(transaction_type='commit'):
        """
        Apply commit or rollback on the current transaction
        """

        try:
            getattr(transaction, transaction_type)()
        except transaction.TransactionManagementError:
            pass  # This code isn't under transaction management

    def _finish_instance(self, table, status=SUCCESS):
        """
        Update the table log instance with the process result.
        """

        if self.errors:
            status = ERROR

        table.status = status
        table.errors = self.errors
        table.logs_deleted = self.logs_deleted
        table.total_logs_deleted += self.logs_deleted
        table.last_executed = self.get_current_date()
        table.updated_by = self.user
        table.save()
