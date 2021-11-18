from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name',
                    'last_name', 'confirmation_code', 'role')
    search_fields = ('username', 'first_name', 'last_name')
    empty_value_display = '--empty--'
