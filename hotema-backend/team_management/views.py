from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from customuser.models import CustomUser


# Serializer untuk memastikan format data konsisten
class UserWithoutRoleSerializer(serializers.ModelSerializer):
    pictures = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['user_id', 'username', 'fullname', 'email', 'role', 'pictures']

    def get_pictures(self, obj):
        request = self.context.get('request')
        if obj.pictures:
            return request.build_absolute_uri(obj.pictures.url)
        return None


class UsersWithoutRoleView(APIView):
    permission_classes = [IsAuthenticated]  # hapus jika mau publik

    def get(self, request):
        # Ambil user yang role-nya NULL atau string kosong
        users = CustomUser.objects.filter(
            Q(role__isnull=True) | Q(role="")
        ).distinct()

        # Serialize data dengan context request agar bisa buat full URL foto
        serializer = UserWithoutRoleSerializer(users, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)
