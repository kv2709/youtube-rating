from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from api_app.models import Youtube
from api_app.serializers import YoutubeSerializer




# Create your views here.
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def youtube_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        youtube_channels = Youtube.objects.all()
        serializer = YoutubeSerializer(youtube_channels, many=True)
        return JSONResponse(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = YoutubeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def youtube_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        youtube_channel = Youtube.objects.get(pk=pk)
    except Youtube.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = YoutubeSerializer(youtube_channel)
        return JSONResponse(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = YoutubeSerializer(youtube_channel, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        youtube_channel.delete()
        return HttpResponse(status=204)

