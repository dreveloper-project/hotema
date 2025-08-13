from rest_framework import serializers
from customuser.models import CustomUser


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
