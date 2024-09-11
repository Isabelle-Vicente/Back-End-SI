from rest_framework import serializers
from .models import Notice

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'
        extra_kwargs = {
            'id_user': {'read_only': True},  # Exclui id_user da criação
            'responsible': {'read_only': True}  # Exclui responsible da criação
        }
