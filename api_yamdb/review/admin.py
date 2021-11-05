from django.contrib import admin
from .models import Title, Review, Comments, Rating


admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comments)
admin.site.register(Rating)
