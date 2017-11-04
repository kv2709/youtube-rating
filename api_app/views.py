from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
import json
from api_app.models import Youtube
from api_app.serializers import YoutubeSerializer

@api_view(['GET','POST'])
@parser_classes((JSONParser,))
def youtube_list(request, format=None):
    """
    List all channels, or create a new channel.
    """
    if request.method == 'GET':
        print("Get")
        query_str = request.environ['QUERY_STRING']
        cont_type = request.environ['CONTENT_TYPE']
        request_dict = {}

        request_dict['country_code'] = request.GET.get('country_code', '')
        request_dict['age_group'] = request.GET.get('age_group', '')
        request_dict['gender'] = request.GET.get('gender', '')
        request_dict['device_type'] = request.GET.get('device_type','')
        request_dict['os'] = request.GET.get('os','')
        print(request_dict)


        youtube_channels = Youtube.objects.all()
        serializer = YoutubeSerializer(youtube_channels, many=True)

        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = YoutubeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def youtube_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code channel.
    """
    try:
        youtube_channel = Youtube.objects.get(pk=pk)
    except Youtube.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = YoutubeSerializer(youtube_channel)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = YoutubeSerializer(youtube_channel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        youtube_channel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

