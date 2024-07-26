import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserProfile
from .serializer import UserProfileSerializer

AUTH_SERVICE_URL = 'http://localhost:8001/api/verify-token/'


class UserProfileListCreateView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization')
        if not token:
            return Response({"error": "Authorization header missing"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = requests.post(AUTH_SERVICE_URL, json={"token": token})
            response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code

            if response.json().get('valid'):
                user_profiles = UserProfile.objects.all()
                serializer = UserProfileSerializer(user_profiles, many=True)
                return Response(serializer.data)
            else:
                return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        except requests.exceptions.RequestException as e:
            return Response({"error": "Authentication service error", "details": str(e)},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def post(self, request):
        token = request.headers.get('Authorization')
        response = requests.post(AUTH_SERVICE_URL, json={"token": token})

        if response.json().get('valid'):
            serializer = UserProfileSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
