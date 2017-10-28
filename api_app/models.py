from django.db import models

# Create your models here.
class Youtube(models.Model):
    name = models.CharField(max_length=255)
    title = models.TextField(blank=True, null=True)
    view_rate = models.DecimalField(default=0, max_digits=14, decimal_places=7)

    def __str__(self):
        """Return string value model"""
        return str(self.name)

class YoutubeGeoAnalytics(models.Model):
    class Meta:
        unique_together = (('youtube_channel', 'country_code', ),)
    youtube_channel = models.ForeignKey(Youtube, related_name='country_views')
    country_code = models.CharField(max_length=5)
    viewer_percentage = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    def __str__(self):
        """Return string value model"""
        return "GeoAnalytics - "+ str(self.youtube_channel) + " - " + \
            self.country_code + " - " + str(self.viewer_percentage)

class YoutubeSexAnalytics(models.Model):
    class Meta:
        unique_together = (('youtube_channel', 'gender', ),)
    youtube_channel = models.ForeignKey(Youtube, related_name='gender_views')
    gender = models.CharField(max_length=10)
    viewer_percentage = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    def __str__(self):
        """Return string value model"""
        return "SexAnalytics - " + str(self.youtube_channel) + " - " + \
            self.gender + " - " + str(self.viewer_percentage)

class YoutubeAgeGroupAnalytics(models.Model):
    class Meta:
        unique_together = (('youtube_channel', 'age_group', ),)
    youtube_channel = models.ForeignKey(Youtube, related_name='age_views')
    age_group = models.CharField(max_length=10)
    viewer_percentage = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    def __str__(self):
        """Return string value model"""
        return "AgeGroupAnalytics " + str(self.youtube_channel) + " - " + \
            self.age_group + " - " + str(self.viewer_percentage)

class YoutubeDeviceAnalytics(models.Model):
    class Meta:
        unique_together = (('youtube_channel', 'device_type', ),)
    youtube_channel = models.ForeignKey(Youtube, related_name='device_views')
    device_type = models.CharField(max_length=50)
    viewer_percentage = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    def __str__(self):
        """Return string value model"""
        return "DeviceAnalytics - " + str(self.youtube_channel) + " - " + \
            self.device_type + " - " + str(self.viewer_percentage)

class YoutubeOSAnalytics(models.Model):
    class Meta:
        unique_together = (('youtube_channel', 'os', ),)
    youtube_channel = models.ForeignKey(Youtube, related_name='os_views')
    os = models.CharField(max_length=50)
    viewer_percentage = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    def __str__(self):
        """Return string value model"""
        return "OSAnalytics - " + str(self.youtube_channel) + " - " + \
            self.os + " - " + str(self.viewer_percentage)

