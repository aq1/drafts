from django.contrib import admin

from will_beams.models import Webm, Tag, WebmTag


class WebmAdmin(admin.ModelAdmin):
    fields = ['video', 'rating', 'nsfw']
    readonly = ['md5']
    list_display = ['video', 'rating', 'md5', 'is_safe_for_work']

admin.site.register(Webm, WebmAdmin)
admin.site.register(Tag)
admin.site.register(WebmTag)

# for model in (Webm, Tag, WebmTag):
#     admin.site.register(model)
