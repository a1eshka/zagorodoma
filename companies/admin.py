from django.contrib import admin
from .models import Constcomp, Services

class ConstcompAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', ]

@admin.register(Constcomp)
class ConstcompAdmin (admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
@admin.register(Services)
class ServicesAdmin (admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
