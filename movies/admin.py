from django.contrib import admin
from .models import Movie, Review
from django.utils.html import format_html

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

    list_display = ['name']
    readonly_fields = ['image_tag']

    def image_tag(self, obj):
        return format_html('<img src="{}" height="200px" />'.format(obj.image.url))
    image_tag.short_description = 'Image'

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
