from django.contrib import admin

from .models import TaskModel

# Register your models here.


class filter(admin.SimpleListFilter):
    title = 'Search filters'
    parameter_name = 'filters'

    def lookups(self, request, model_admin):
        return [
            ('complete', 'Completed'),
            ('not_complete', 'Active'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'complete':
            return queryset.filter(complete=True)
        return None


@admin.register(TaskModel)
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('id', )
    list_display = ['name', 'created_at', 'complete']
    list_filter = (filter, )
    fields = ['id', 'name', 'complete', 'user']
    search_fields = ['name__startswith']

