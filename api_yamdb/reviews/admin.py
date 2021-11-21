from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class UserAdmin(admin.ModelAdmin):
    list_display = ("pk", "email", "bio", "confirmation_code", "role")


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'year', 'description', 'category', 'name')
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'title', 'text')
    search_fields = ('author',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'review', 'text')
    search_fields = ('author',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentsAdmin)
admin.site.register(Category)
admin.site.register(Genre)
