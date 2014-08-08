"""
Views file for django app edxval.
"""

from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view


from edxval.models import Video, Profile
from edxval.serializers import (
    VideoSerializer,
    ProfileSerializer
)


class VideoList(generics.ListCreateAPIView):
    """
    GETs or POST video objects
    """
    queryset = Video.objects.all().prefetch_related("encoded_videos")
    lookup_field = "edx_video_id"
    serializer_class = VideoSerializer

    def create(self, request, *args, **kwargs):
        bulk = isinstance(request.DATA, list)

        if not bulk:
            return mixins.CreateModelMixin.create(self, request, *args, **kwargs)

        else:
            serializer = self.get_serializer(data=request.DATA, many=True)
            print serializer.errors
            if serializer.is_valid():
                [self.pre_save(obj) for obj in serializer.object]
                self.object = serializer.save(force_insert=True)
                [self.post_save(obj, created=True) for obj in self.object]
                return Response(data = {"encoded_videos":"meow"}, status=status.HTTP_201_CREATED)
        print "yatta"
        self.request._data = {"Success":"success"}
        print self.request._data
        return Response(data= serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileList(generics.ListCreateAPIView):
    """
    GETs or POST video objects
    """
    queryset = Profile.objects.all()
    lookup_field = "profile_name"
    serializer_class = ProfileSerializer


class VideoDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Gets a video instance given its edx_video_id
    """
    lookup_field = "edx_video_id"
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
