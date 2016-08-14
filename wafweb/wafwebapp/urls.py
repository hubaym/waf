from django.conf.urls import url
from django.conf.urls import (
handler400, handler403, handler404, handler500
)
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^results/$', views.results, name='results'),
    url(r'^login/$', views.login, name='login'),
    url(r'^registration/$', views.registration, name='registration'),
    url(r'^auth/$', views.auth_view, name='auth_view'),    
]


handler400 = 'views.bad_request'
handler403 = 'views.permission_denied'
handler404 = 'views.page_not_found'
handler500 = 'views.server_error'