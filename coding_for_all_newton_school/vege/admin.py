from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.utils.safestring import mark_safe


# class ReceipeModel(admin.ModelAdmin):
#     list_display = [
#         field.name for field in Recipe._meta.get_fields()
#     ]

class ReceipeModel(admin.ModelAdmin):
    list_display = (
        'id',
        'receipe_name',
        'receipe_description',
        'receipe_image',
        'user_id',
    )
    list_display_links  = (
        'id',
        'receipe_image'
    )
    search_fields = ('receipe_name', 'receipe_description')
    list_filter = ['receipe_name'] 
    
    def image_tag(self,obj):
        return format_html('<img src="{}" width="50" height="50" />'.format(obj.receipe_image.url))
    image_tag.short_description = 'Image'

admin.site.register(Recipe, ReceipeModel)