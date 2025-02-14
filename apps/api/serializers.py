from rest_framework import serializers

from apps.api.models import *
from apps.auths.serializers import UserSerializer


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
      model = Task
      fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    task = TaskSerializer(read_only=True)
    class Meta:
      model = TaskComment
      fields = '__all__'

class TaskCommentSerializer(serializers.Serializer):
    comment = serializers.CharField(max_length=255, required=True)

