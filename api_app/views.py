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
    #---------------------0:00:00.816047----------------------------------------------
    youtube_query_set = Youtube.objects.all()
    for youtube_channel in youtube_query_set:
        name_channel_l = youtube_channel.name
        count_views_channel = float(Youtube.objects.get(name = name_channel_l).view_rate)
        # ----------------------geo------------------------------------------------------------
        list_dict_geo_unique = YoutubeGeoAnalytics.objects.all().values("country_code").distinct()
        list_geo_unique = []
        for i in range(len(list_dict_geo_unique)):
            list_geo_unique.append(list_dict_geo_unique[i]["country_code"])
        if geo != '' and geo not in list_geo_unique:
            return False
        if geo != '':
            rating_geo = float(Youtube.objects.get(name=name_channel_l).country_views.filter(country_code=geo).
                               values("viewer_percentage")[0]['viewer_percentage'])
        else:
            rating_geo = 1
        #----------------------age------------------------------------------------------------
        list_dict_age_unique = YoutubeAgeGroupAnalytics.objects.all().values("age_group").distinct()
        list_age_unique = []
        for i in range(len(list_dict_age_unique)):
            list_age_unique.append(list_dict_age_unique[i]["age_group"])
        if age != '' and age not in list_age_unique:
            return False
        if age != '':
            rating_age = float(Youtube.objects.get(name=name_channel_l).age_views.filter(age_group=age).
                               values("viewer_percentage")[0]['viewer_percentage'])
        else:
            rating_age = 1
        #----------------------gender------------------------------------------------------------
        list_dict_gender_unique = YoutubeSexAnalytics.objects.all().values("gender").distinct()
        list_gender_unique = []
        for i in range(len(list_dict_gender_unique)):
            list_gender_unique.append(list_dict_gender_unique[i]["gender"])
        if gen != '' and gen not in list_gender_unique:
            return False
        if gen != '':
            rating_gen = float(Youtube.objects.get(name=name_channel_l).gender_views.filter(gender=gen).
                               values("viewer_percentage")[0]['viewer_percentage'])
        else:
            rating_gen = 1
        #---------------------------device-------------------------------------------------
        list_dict_device_unique = YoutubeDeviceAnalytics.objects.all().values("device_type").distinct()
        list_device_unique = []
        for i in range(len(list_dict_device_unique)):
            list_device_unique.append(list_dict_device_unique[i]["device_type"])
        if dev != '' and dev not in list_device_unique:
            return False
        if dev != '':
            rating_dev = float(Youtube.objects.get(name=name_channel_l).device_views.filter(device_type=dev).
                               values("viewer_percentage")[0]['viewer_percentage'])
        else:
            rating_dev = 1
        #------------------------------OS---------------------------------------------
        list_dict_os_unique = YoutubeOSAnalytics.objects.all().values("os").distinct()
        list_os_unique = []
        for i in range(len(list_dict_os_unique)):
            list_os_unique.append(list_dict_os_unique[i]["os"])
        if osd != '' and osd not in list_os_unique:
            return False
        if osd != '':
            rating_osd = float(Youtube.objects.get(name=name_channel_l).os_views.filter(os=osd).
                               values("viewer_percentage")[0]['viewer_percentage'])
        else:
            rating_osd = 1
        #------------------------------------------------------------------------------------
        sum_rating = count_views_channel * rating_geo * rating_age * \
                     rating_gen * rating_dev * rating_osd
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
    return True




@api_view(['GET'])
def youtube_list(request, format=None):
    """
    List all channels, or create a new channel.
    """
    if request.method == 'GET':
        query_str = request.environ['QUERY_STRING']
        cont_type = request.environ['CONTENT_TYPE']
        request_dict = {}
        res = False
        if query_str != "":
            request_dict['country_code'] = request.GET.get('country_code', '')
            request_dict['age_group'] = request.GET.get('age_group', '')
            request_dict['gender'] = request.GET.get('gender', '')
            request_dict['device_type'] = request.GET.get('device_type', '')
            request_dict['os'] = request.GET.get('os', '')
            res = calculate_rating(request_dict)
        if res or query_str == "":
            youtube_channels = Youtube.objects.all()
            youtube_channels_sort = youtube_channels.order_by("calc_rate_request").reverse()
            serializer = YoutubeSerializer(youtube_channels_sort, many=True)
            return Response(serializer.data)
        else:
            error_dict = {"result_request": "Error in value argument"}
            return Response(error_dict)

    # elif request.method == 'POST':
    #     serializer = YoutubeSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def youtube_filter(request, format=None):
    """
    Filter channels on count viewers.
    """
    if request.method == 'GET':
        query_str = request.environ['QUERY_STRING']
        if query_str != "":
            range_filter_str = request.GET.get('range', '')
            try:
                list_range = range_filter_str.split("-")
                beg_range = float(list_range[0])
                end_range = float(list_range[1])
                youtube_channels = Youtube.objects.all()
                youtube_channels_filter = youtube_channels.filter(view_rate__gte=beg_range, view_rate__lte=end_range)
                serializer = YoutubeSerializer(youtube_channels_filter, many=True)
                return Response(serializer.data)
            except:
                error_dict = {"result_request": "Error in value argument"}
                return Response(error_dict)
        else:
            youtube_channels = Youtube.objects.all()
            serializer = YoutubeSerializer(youtube_channels, many=True)
            return Response(serializer.data)



@api_view(['GET', 'PUT', 'DELETE'])
def youtube_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code channel.
    """
    try:
        if int(pk) % 2 == 0:
            youtube_channel = Youtube.objects.get(pk=pk)
        else:
            error_dict = {'Error access': 'Access is allowed only to fields with an even id value'}
            return Response(error_dict)
    except Youtube.DoesNotExist:
        error_dict = {'Error access': 'Model with id='+ str(pk) + ' does not exist'}
        return Response(error_dict)#status=status.HTTP_404_NOT_FOUND
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