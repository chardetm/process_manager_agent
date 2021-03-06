from rest_framework import serializers
from models import Op
import django.contrib.auth


class UserSerializer(serializers.ModelSerializer):
    ops = serializers.PrimaryKeyRelatedField(many=True, queryset=Op.objects.all())

    class Meta:
        model = django.contrib.auth.get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'is_active',
                  'date_joined', 'password', 'ops',)
        read_only_fields = ('id', 'is_staff', 'is_superuser', 'is_active', 'date_joined', 'ops')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self, **kwargs):
        from django.contrib.auth.models import User
        User.objects.create_user(self.initial_data["username"], password=self.initial_data["password"])


class OpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Op
        fields = ('id', 'user', 'script', 'callback_url', 'status', 'info')
        read_only_fields = ('id', 'user', 'status', 'info')

