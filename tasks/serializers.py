from rest_framework import serializers
from .models import TaskApi


class TaskApiSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskApi
        fields = '__all__'
        read_only_fields = ['user']

    def validate_title(self, value):
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Title must be at least 3 characters long."
            )

        return value