from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from customuser.models import CustomUser
from .serializers import UserWithoutRoleSerializer
import os



class UsersWithoutRoleView(APIView):
    permission_classes = [IsAuthenticated]  

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
    
class UsersByRoleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        role = request.query_params.get('role')
        allowed_roles = ["staff", "supervisor"]

        if not role or role.lower() not in allowed_roles:
            return Response(
                {"error": f"Role harus salah satu dari: {allowed_roles}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        users = CustomUser.objects.filter(role__iexact=role).distinct()
        serializer = UserWithoutRoleSerializer(
            users, many=True, context={'request': request}  # ⬅ penting untuk URL foto
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = CustomUser.objects.get(user_id=user_id)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User tidak ditemukan."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = UserWithoutRoleSerializer(
            user, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):
        try:
            user = CustomUser.objects.get(user_id=user_id)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User tidak ditemukan."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Hapus file profile_pictures jika ada
        if user.pictures and user.pictures.path:
            if os.path.isfile(user.pictures.path):
                os.remove(user.pictures.path)

        # Baru hapus user di DB
        user.delete()

        return Response(
            {"message": f"User dengan ID {user_id} berhasil dihapus beserta profile picture."},
            status=status.HTTP_204_NO_CONTENT
        )


class UpdateUserRoleByIdView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, user_id, *args, **kwargs):
        new_role = request.data.get("role")

        # Validasi input
        if not new_role:
            return Response(
                {"error": "Field 'role' harus dikirim."},
                status=status.HTTP_400_BAD_REQUEST
            )

        allowed_roles = ["staff", "supervisor"]
        if new_role.lower() not in allowed_roles:
            return Response(
                {"error": f"Role harus salah satu dari: {allowed_roles}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = CustomUser.objects.get(user_id=user_id)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User tidak ditemukan."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Update role
        user.role = new_role
        user.save()

        return Response(
            {
                "message": "Role user berhasil diperbarui.",
                "user_id": user.user_id,
                "fullname": user.fullname,
                "role": user.role
            },
            status=status.HTTP_200_OK
        )