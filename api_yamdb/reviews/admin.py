from django.contrib import admin
from .models import User, Title, Review, Comments, Category, Genre

from django.contrib import admin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'role')
    search_fields = ('username', 'first_name', 'last_name')
    empty_value_display = '--empty--'


class UserAdmin(admin.ModelAdmin):
    list_display = ("pk", "email", "bio", "confirmation_code", "role")


admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comments)
admin.site.register(Category)
admin.site.register(Genre)
