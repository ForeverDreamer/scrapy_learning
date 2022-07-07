from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^ri$', request_info),
    url(r'^ps$', proxy_server),
]