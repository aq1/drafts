from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static


from will_beams.views import index


if settings.DEBUG:
    urlpatterns = static(settings.MEDIA_URL,
                         document_root=settings.MEDIA_ROOT)
else:
    urlpatterns = []

urlpatterns += [
    url(r'', index),
]
