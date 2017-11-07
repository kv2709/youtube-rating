from django.conf.urls import url
from api_app import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', views.index),
    url(r'^api_app/$', views.youtube_list),
    url(r'^api_app/(?P<pk>[0-9]+)/$', views.youtube_detail),]

urlpatterns = format_suffix_patterns(urlpatterns)