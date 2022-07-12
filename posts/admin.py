from django.contrib import admin
from .models import Post_sale, Status, Land_status, Heating, House_material, Type_object, Water, PostImage

class PostsAdmin (admin.ModelAdmin):
    list_display = ('id', 'status', 'created_at', 'price')
    list_display_links = ('id', 'status')
    search_fields = ('id',)

admin.site.register(Post_sale, PostsAdmin)
admin.site.register(Heating)
admin.site.register(Land_status)
admin.site.register(House_material)
admin.site.register(Water)
admin.site.register(PostImage)

@admin.register(Type_object)
class Type_objectAdmin (admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Status)
class StatusAdmin (admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
   







