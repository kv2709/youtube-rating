from django.conf.urls import url
from api_app import views

urlpatterns = [
    url(r'^api_app/$', views.youtube_list),
    url(r'^api_app/(?P<pk>[0-9]+)/$', views.youtube_detail),]