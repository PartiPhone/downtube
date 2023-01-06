from django.contrib import admin

from .models import Video


class VideoAdmin(admin.ModelAdmin):
    list_display = ["user", "title", "url"]
    search_fields = ["title"]
    readonly_fields = ["user"]
    ordering = ["user"]


admin.site.register(Video, VideoAdmin)
