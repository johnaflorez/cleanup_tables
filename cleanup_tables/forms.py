import os

from django import forms
from django.conf import settings

from cleanup_tables.choices import CLEAN_UP_PERIOD_TIME_OPTIONS
from cleanup_tables.models import CleanUPTables, ModelDoesNotExist


class CleanUPTablesForm(forms.ModelForm):
    """
    Form to handle the Clean-UP table logs registration process
    """

    table_name = forms.ChoiceField(label='Table Name', required=True)

    class Meta:
        model = CleanUPTables
        fields = ('table_name', 'date_field', 'clean_up_rule', 'sql_file', 'priority', 'active')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CleanUPTablesForm, self).__init__(*args, **kwargs)
        choices = [(model_name, model_name) for model_name in settings.VALID_MODELS_TO_CLEAN_UP]
        self.sql_extensions = ['.sql']
        self.fields['table_name'].choices = [('', '-------')] + choices
        self.model = None

    def clean_table_name(self):
        try:
            table_name = self.cleaned_data.get('table_name')
            self.model = CleanUPTables.get_model_class(table_name)
            return table_name
        except ModelDoesNotExist as err:
            raise forms.ValidationError(err.__unicode__())

    def clean_date_field(self):
        date_field = self.cleaned_data.get('date_field')
        if not CleanUPTables.model_field_exists(self.model, date_field):
            raise forms.ValidationError(
                'Field {0} does not exists in model {1}.'.format(date_field, self.model.__name__)
            )

        if not CleanUPTables.is_date_field(self.model, date_field):
            raise forms.ValidationError(
                'Field {0} is not date time type.'.format(date_field)
            )
        return date_field

    def clean_clean_up_rule(self):
        clean_up_rule = self.cleaned_data.get('clean_up_rule')
        quantity, period_time = clean_up_rule.split('_')
        if not quantity.isdigit() and period_time not in CLEAN_UP_PERIOD_TIME_OPTIONS.values():
            raise forms.ValidationError(
                'Cleanup rule {0} has an invalid structure.'.format(clean_up_rule)
            )
        return clean_up_rule

    def clean_sql_file(self):
        sql_file = self.cleaned_data.get('sql_file')
        if sql_file:
            extension = os.path.splitext(sql_file.name)[1].lower()
            if extension not in self.sql_extensions:
                raise forms.ValidationError(
                    'The file uploaded has no extension .sql'
                )
        return sql_file

    def save(self, commit=False):
        instance = super(CleanUPTablesForm, self).save(commit)
        instance.created_by = self.user
        if instance.pk:
            instance.updated_by = self.user
        instance.save()
        return instance
