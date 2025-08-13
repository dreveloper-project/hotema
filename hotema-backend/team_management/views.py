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

class UpdateUserRoleView(APIView):
    permission_classes = [IsAuthenticated] 

    def patch(self, request, *args, **kwargs):
        user_id = request.data.get("user_id")
        new_role = request.data.get("role")

        # Validasi input
        if not user_id or not new_role:
            return Response(
                {"error": "user_id dan role harus dikirim."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Pastikan role valid
        allowed_roles = ["staff", "supervisor"]
        if new_role.lower() not in allowed_roles:
            return Response(
                {"error": f"Role harus salah satu dari: {allowed_roles}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = CustomUser.objects.get(user_id=user_id, role__isnull=True)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User tidak ditemukan atau role sudah terisi."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Update role
        user.role = new_role
        user.save()

        return Response(
            {
                "message": "Role berhasil diperbarui.",
                "user_id": user.user_id,
                "fullname": user.fullname,
                "role": user.role
            },
            status=status.HTTP_200_OK
        )