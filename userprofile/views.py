from django.http import JsonResponse
from django.views import View
from django.utils.decorators import classonlymethod
from asgiref.sync import sync_to_async
from .models import UserProfile
from .serializer import UserProfileSerializer


class UserProfileListCreateView(View):
    @classonlymethod
    async def get(cls, request):
        user_profiles = await sync_to_async(UserProfile.objects.all)()
        serialized_data = UserProfileSerializer().serialize(user_profiles)
        return JsonResponse(serialized_data, safe=False)

    @classonlymethod
    async def post(cls, request):
        data = request.POST
        user_profile = await sync_to_async(UserProfile.objects.create)(
            username=data['username'],
            email=data['email'],
            bio=data['bio']
        )
        serialized_data = UserProfileSerializer().serialize([user_profile])
        await send_user_profile.delay(serialized_data)
        return JsonResponse(serialized_data, safe=False)
