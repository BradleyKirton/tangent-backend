from django.urls import re_path
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from channels.http import AsgiHandler
from accounts import routing


application = ProtocolTypeRouter({
    'http': URLRouter(routing.urlpatterns + [re_path('^', AsgiHandler)])
})