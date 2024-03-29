from django.conf import settings
from django.contrib import admin

from .models import Group, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Сustom admin panel for Post."""
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
    )
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass
