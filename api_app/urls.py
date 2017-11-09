from django.conf.urls import url
from api_app import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', views.index),
    url(r'^channel/$', views.youtube_list),
    url(r'^channel/(?P<pk>\d+)/$', views.youtube_detail),
    url(r'^channel_filter/$', views.youtube_filter),
]

urlpatterns = format_suffix_patterns(urlpatterns)