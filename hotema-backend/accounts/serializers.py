from rest_framework import serializers
from customuser.models import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.db import transaction

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'fullname', 'password', 'password2', 'pictures')  # Hapus 'role'

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def validate_pictures(self, value):
        allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
        max_size = 2 * 1024 * 1024  # 2MB

        if value:
            if value.content_type not in allowed_types:
                raise serializers.ValidationError("Hanya file JPG, JPEG, atau PNG yang diperbolehkan.")
            if value.size > max_size:
                raise serializers.ValidationError("Ukuran gambar maksimal 2MB.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop('password2')
        pictures = validated_data.pop('pictures', None)

        # Role akan di-set dari RegisterView, bukan dari data ini
        user = CustomUser.objects.create_user(**validated_data)

        if pictures:
            user.pictures = pictures
            user.save()

        return user
