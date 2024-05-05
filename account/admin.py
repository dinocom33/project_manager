from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_staff')
    list_filter = ('email', 'name', 'is_staff', 'is_superuser')
    search_fields = ('name', 'email')
