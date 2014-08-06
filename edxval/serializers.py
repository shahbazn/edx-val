"""
Serializers for Video Abstraction Layer
"""
from rest_framework import serializers

from edxval.models import Profile, Video, EncodedVideo


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Profile object.
    """
    class Meta: # pylint: disable=C1001, C0111
        model = Profile
        fields = (
            "profile_name",
            "extension",
            "width",
            "height"
        )


class EncodedVideoSerializer(serializers.ModelSerializer):
    """
    Serializer for EncodedVideo object.

    Uses the profile_name as it's profile value instead of a Profile object.
    """
    profile = serializers.SlugRelatedField(slug_field="profile_name")

    class Meta: # pylint: disable=C1001, C0111
        model = EncodedVideo
        fields = (
            "created",
            "modified",
            "url",
            "file_size",
            "bitrate",
            "profile",
        )

    def get_identity(self, data):
        """
        This hook is required for bulk update.
        We need to override the default, to use the slug as the identity.

        Note that the data has not yet been validated at this point,
        so we need to deal gracefully with incorrect datatypes.
        """
        try:
            return data.get('profile', None)
        except AttributeError:
            return None


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Video object

    encoded_videos takes a list of dicts EncodedVideo data.
    """
    encoded_videos = EncodedVideoSerializer(many=True, allow_add_remove=True)

    class Meta: # pylint: disable=C1001,C0111
        model = Video
        lookup_field = "edx_video_id"
