import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.template.defaultfilters import slugify

from cleanup_tables.choices import (
    CLEAN_UP_PERIOD_TIME_OPTIONS, HOUR, DAY, WEEK, MONTH, YEAR,
    CLEAN_UP_STATUS_OPTIONS, NEW,
    CLEAN_UP_PRIORITY_OPTIONS, NORMAL
)
from cleanup_tables.constants import CleanUPTableHelpTextModel
from cleanup_tables.exceptions import ModelDoesNotExist, DateFormatException


class CleanUPTables(models.Model):
    """
    Model to manage the models to clean up
    """

    def get_upload_path(self, filename):
        now = datetime.now()
        return os.path.join(
            'cleanup_files', slugify(self.table_name), str(now.year), str(now.month), filename
        )

    table_name = models.CharField(max_length=255, unique=True, help_text=CleanUPTableHelpTextModel.TABLE_NAME)
    date_field = models.CharField(max_length=255, help_text=CleanUPTableHelpTextModel.DATE_FIELD)
    clean_up_rule = models.CharField(max_length=255, help_text=CleanUPTableHelpTextModel.CLEAN_UP_RULE)
    sql_file = models.FileField(null=True, blank=True, upload_to=get_upload_path)
    priority = models.CharField(
        max_length=100,
        choices=CLEAN_UP_PRIORITY_OPTIONS,
        default=NORMAL,
        help_text=CleanUPTableHelpTextModel.PRIORITY
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', related_name='clean_up_created_by', null=True, blank=True,
                                   on_delete=models.SET_NULL)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True, null=True, blank=True)
    updated_by = models.ForeignKey('auth.User', related_name='clean_up_updated_by', null=True, blank=True,
                                   on_delete=models.SET_NULL)
    last_executed = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    status = models.CharField(max_length=100, choices=CLEAN_UP_STATUS_OPTIONS, default=NEW)
    logs_deleted = models.BigIntegerField(default=0)
    total_logs_deleted = models.BigIntegerField(default=0)
    errors = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return u'{0}'.format(self.table_name)

    def save(self, **kwargs):
        if not self.pk:
            self.updated_at = None
        super(CleanUPTables, self).save(**kwargs)

    @classmethod
    def get_model_class(cls, table_name):
        """
        Get model class from the `table_name`

        Args:
            table_name (String): model name definition
        """

        try:
            content_type = ContentType.objects.filter(model=table_name.lower()).latest('id')
            return content_type.model_class()
        except ContentType.DoesNotExist:
            raise ModelDoesNotExist(table_name)

    @classmethod
    def model_field_exists(cls, model, field_name):
        """
        Validate if the `field_name` (date_field) exists in the `model` (table_name)

        Args:
            model (ModelBase): model Class to validate
            field_name (String): field name to check existence in the model
        """

        try:
            model._meta.get_field(field_name)
            return True
        except FieldDoesNotExist:
            return False

    @classmethod
    def is_date_field(cls, model, field_name):
        """
        Validate if the field_name is date_time/date type.
        """

        return model._meta.get_field(field_name).__class__ in [models.DateTimeField, models.DateField]

    def get_date(self):
        """
        Build date from the `clean_up_rule` defined
        """

        current_date = datetime.now()
        keep_hours = False
        quantity, period_time = self.clean_up_rule.split('_')
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
            raise DateFormatException(self.clean_up_rule)

        if keep_hours:
            return _date
        return datetime.combine(_date, datetime.max.time())
