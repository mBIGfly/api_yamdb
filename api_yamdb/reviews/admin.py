
from django.contrib import admin

from .models import Category, Comments, Review, Title

admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comments)
admin.site.register(Category)
