from rest_framework import serializers
from api_app.models import Youtube


class YoutubeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Youtube
        fields = ('id', 'name', 'title', 'view_rate')

    def create(self, validated_data):
        """
        Create and return a new `Youtube` instance, given the validated data.
        """
        return Youtube.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Youtube` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.title = validated_data.get('title', instance.title)
        instance.view_rate = validated_data.get('view_rate', instance.view_rate)

        instance.save()
        return instance