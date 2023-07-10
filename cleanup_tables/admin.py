from django.contrib import admin, messages

from cleanup_tables.forms import CleanUPTablesForm
from cleanup_tables.models import CleanUPTables


class CleanUPTablesAdmin(admin.ModelAdmin):
    form = CleanUPTablesForm
    actions = ['launch_cleanup_process']
    list_display = (
        'table_name',
        'date_field',
        'clean_up_rule',
        'priority',
        'sql_file',
        'created_at',
        'last_executed',
        'updated_at',
        'status',
        'logs_deleted',
        'total_logs_deleted',
        'errors'
    )
    list_filter = ('status', 'priority', 'clean_up_rule')
    raw_id_fields = ('created_by', 'updated_by')
    search_fields = ('table_name', 'date_field')

    def launch_cleanup_process(self, request, queryset):
        """
        Launch manually the cleanup process
        """

        from cleanup_tables.core import CleanUPTablesManager

        for query in queryset:
            manager = CleanUPTablesManager(instance_id=query.id)
            manager.cleanup()
        messages.success(request, 'Cleanup process launched successfully.')

    launch_cleanup_process.short_description = "Launch CleanUP Process"


admin.site.register(CleanUPTables, CleanUPTablesAdmin)
