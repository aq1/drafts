from django.conf.urls import include, url
from django.contrib import admin

from will_beams.views import index

urlpatterns = [
    url(r'', index),
]
