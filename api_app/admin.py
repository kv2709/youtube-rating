from django.contrib import admin
from api_app.models import Youtube
from api_app.models import YoutubeAgeGroupAnalytics
from api_app.models import YoutubeDeviceAnalytics
from api_app.models import YoutubeSexAnalytics
from api_app.models import YoutubeGeoAnalytics
from api_app.models import YoutubeOSAnalytics

# Register your models here.
admin.site.register(Youtube)
admin.site.register(YoutubeAgeGroupAnalytics)
admin.site.register(YoutubeDeviceAnalytics)
admin.site.register(YoutubeSexAnalytics)
admin.site.register(YoutubeGeoAnalytics)
admin.site.register(YoutubeOSAnalytics)