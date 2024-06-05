from django.contrib import admin

from todolist.models import ToDoList


@admin.register(ToDoList)
class TodoListAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    list_filter = ('name', 'created_at')
    search_fields = ('name',)
