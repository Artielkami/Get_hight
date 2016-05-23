from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^new/$', views.new, name='update'),
    url(r'^up/(?P<rs_path_id>[0-9]+)/$', views.update, name='up'),
    url(r'^$', views.index, name='index'),
]

urlpatterns += staticfiles_urlpatterns()
