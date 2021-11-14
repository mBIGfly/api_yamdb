from django.contrib import admin
from .models import User, Title, Review, Comments, Category


class UserAdmin(admin.ModelAdmin):
    list_display = ("pk", "email", "bio", "confirmation_code", "role")


admin.site.register(User, UserAdmin)
admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comments)
admin.site.register(Category)
