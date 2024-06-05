from django.contrib import admin

from task.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'status', 'created_at', 'updated_at')
    list_filter = ('name', 'created_at')
    search_fields = ('name',)

