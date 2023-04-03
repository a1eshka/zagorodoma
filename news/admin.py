from django.contrib import admin
from .models import *

class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', ]

@admin.register(News)
class NewsAdmin (admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}