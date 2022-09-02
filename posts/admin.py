from django.contrib import admin
from .models import Post_sale, Status, Land_status, Heating, House_material, Type_object, Water, PostImage, Ip, HouseAdditional, Rent_amenities


def complete_post(modeladmin, reguest, queryset):
    queryset.update(published=True)
complete_post.short_description = 'Опубликовать новости'

def incomplete_post(modeladmin, reguest, queryset):
    queryset.update(published=False)
incomplete_post.short_description = 'Снять с публикации'


class PostsAdmin (admin.ModelAdmin):
    list_display = ('id', 'status', 'created_at', 'price', 'published')
    list_display_links = ('id', 'status')
    search_fields = ('id',)
    actions = (complete_post, incomplete_post)



admin.site.register(Post_sale, PostsAdmin)
admin.site.register(Heating)
admin.site.register(Land_status)
admin.site.register(House_material)
admin.site.register(Water)
admin.site.register(PostImage)
admin.site.register(Ip)


@admin.register(Type_object)
class Type_objectAdmin (admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Status)
class StatusAdmin (admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

@admin.register(HouseAdditional)
class HouseAdditionalAdmin (admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Rent_amenities)
class Rent_amenitiesAdmin (admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)} 







