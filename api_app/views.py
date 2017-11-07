from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api_app.models import Youtube, YoutubeGeoAnalytics, \
    YoutubeSexAnalytics, YoutubeAgeGroupAnalytics, \
    YoutubeDeviceAnalytics, YoutubeOSAnalytics
from api_app.serializers import YoutubeSerializer
import datetime
from django.shortcuts import render

def calculate_rating(request_dict):
    geo = request_dict['country_code']
    age = request_dict['age_group']
    gen = request_dict['gender']
    dev = request_dict['device_type']
    osd = request_dict['os']
    # time_start = datetime.datetime.now()

    #-------------------0:00:00.880051-----------------------------------------------------
    youtube_query_set = Youtube.objects.all()
    for youtube_channel in youtube_query_set:
        name_channel_l = youtube_channel.name
        count_views_channel = float(Youtube.objects.get(name = name_channel_l).view_rate)
        rating_geo = float(Youtube.objects.get(name = name_channel_l).country_views.filter(country_code = geo).values("viewer_percentage")[0]['viewer_percentage'])
        rating_age = float(Youtube.objects.get(name=name_channel_l).age_views.filter(age_group=age).values("viewer_percentage")[0]['viewer_percentage'])
        rating_gen = float(Youtube.objects.get(name=name_channel_l).gender_views.filter(gender=gen).values("viewer_percentage")[0]['viewer_percentage'])
        rating_dev = float(Youtube.objects.get(name=name_channel_l).device_views.filter(device_type=dev).values("viewer_percentage")[0]['viewer_percentage'])
        rating_osd = float(Youtube.objects.get(name=name_channel_l).os_views.filter(os=osd).values("viewer_percentage")[0]['viewer_percentage'])
        sum_rating = count_views_channel * rating_geo * rating_age * rating_gen * rating_dev * rating_osd
        youtube_channel.calc_rate_request = sum_rating
        youtube_channel.save()
    #------------------------------------------------------------------------------------

    #---------------------00:00:00.922053------------------------------------------------
    # youtube_query_set = Youtube.objects.all()
    # for idy in youtube_query_set.values("id"):
    #     i = idy["id"]
    #     rating_geo = float(YoutubeGeoAnalytics.objects.filter(youtube_channel=i, country_code=geo).values("viewer_percentage")[0]['viewer_percentage'])
    #     rating_age = float(YoutubeAgeGroupAnalytics.objects.filter(youtube_channel=i, age_group=age).values("viewer_percentage")[0]['viewer_percentage'])
    #     rating_gen = float(YoutubeSexAnalytics.objects.filter(youtube_channel=i, gender=gen).values("viewer_percentage")[0]['viewer_percentage'])
    #     rating_dev = float(YoutubeDeviceAnalytics.objects.filter(youtube_channel=i, device_type=dev).values("viewer_percentage")[0]['viewer_percentage'])
    #     rating_osd = float(YoutubeOSAnalytics.objects.filter(youtube_channel=i, os=osd).values("viewer_percentage")[0]['viewer_percentage'])
    #     youtube_row = Youtube.objects.get(id=i)
    #     count_views_channel = float(youtube_row.view_rate)
    #     sum_rating = count_views_channel * rating_geo * rating_age * rating_gen * rating_dev * rating_osd
    #     youtube_row.calc_rate_request = sum_rating
    #     youtube_row.save()
    #--------------------------------------------------------------------------
    # time_finish = datetime.datetime.now()
    # print(str(time_finish - time_start))




@api_view(['GET','POST'])
def youtube_list(request, format=None):
    """
    List all channels, or create a new channel.
    """
    if request.method == 'GET':

        query_str = request.environ['QUERY_STRING']
        cont_type = request.environ['CONTENT_TYPE']
        request_dict = {}
        if query_str != "":
            request_dict['country_code'] = request.GET.get('country_code', '')
            request_dict['age_group'] = request.GET.get('age_group', '')
            request_dict['gender'] = request.GET.get('gender', '')
            request_dict['device_type'] = request.GET.get('device_type','')
            request_dict['os'] = request.GET.get('os','')
            calculate_rating(request_dict)

        youtube_channels = Youtube.objects.all()
        youtube_channels_sort = youtube_channels.order_by("calc_rate_request").reverse()
        serializer = YoutubeSerializer(youtube_channels_sort, many=True)
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

def index(request):
    """Home page application"""
    return render(request, 'api_app/index.html')