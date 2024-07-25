from django.core.serializers.json import Serializer as JSONSerializer
from .models import UserProfile


class UserProfileSerializer(JSONSerializer):
    def get_dump_object(self, obj):
        return {
            'id': obj.id,
            'username': obj.username,
            'email': obj.email,
            'bio': obj.bio,
        }
