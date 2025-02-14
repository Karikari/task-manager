from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.email_task import send_email_task
from apps.api.models import Task, TaskComment
from apps.api.permissions import IsTaskOwnerOrAdmin
from apps.api.serializers import TaskSerializer, TaskCommentSerializer, \
  CommentSerializer
# from apps.api.tasks import send_email_task
from apps.auths.models import User
from apps.commons.ModelUtils import get_object_or_None


class TaskView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'due_date']

    @swagger_auto_schema(operation_description="Get All Tasks", responses={200: "Success"})
    def get(self, request):
      tasks = Task.objects.all()
      for backend in self.filter_backends:
        tasks = backend().filter_queryset(request, tasks, self)
      serializer = self.serializer_class(tasks, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="Create Task", responses={200: "Success", 400: "Bad Request"}, request_body=TaskSerializer)
    def post(self, request):
      serializer = self.serializer_class(data=request.data)
      if serializer.is_valid():
        serializer.save()
        # Sending Email
        user = get_object_or_None(User, serializer.data['assign_to'])
        if user:
          subject = "Task #{} Created".format(serializer.data['id']),
          message = "Your Task #{} has been  successfully created".format(serializer.data['id'])
          email_list = [request.user.email, user.email]
          send_email_task.delay(subject, message, email_list)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated, IsTaskOwnerOrAdmin]
    serializer_class = TaskSerializer

    @swagger_auto_schema(operation_description="Get a Task", responses={200: "Success"})
    def get(self, request, id):
      task = get_object_or_None(Task, pk=id)
      if not task:
        return Response(status=status.HTTP_404_NOT_FOUND)
      serializer = self.serializer_class(task)
      return Response(serializer.data)

    @swagger_auto_schema(operation_description="Update a Task", responses={200: "Success", 400: "Bad Request"}, request_body=TaskSerializer)
    def put(self, request, id):
      task = get_object_or_None(Task, pk=id)
      if not task:
        return Response(status=status.HTTP_404_NOT_FOUND)

      # Check if Owner or Admin has permission
      self.check_object_permissions(request, task)

      serializer = self.serializer_class(task, data=request.data)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="Delete a Task", responses={204: "No Content"})
    def delete(self, request, id):
      task = get_object_or_None(Task, pk=id)
      if not task:
        return Response(status=status.HTTP_404_NOT_FOUND)

      # Check if Owner or Admin has permission
      self.check_object_permissions(request, task)

      task.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)

class AssignTaskView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(operation_description="Assign a Task to a User", responses={200: "Success"})
    def get(self, request, task_id, user_id):
      task = get_object_or_None(Task, pk=task_id)
      user = get_object_or_None(User, pk=user_id)
      if task and user:
        task.assign_to = user
        task.save()

        subject = "Task #{} Created".format(task.id),
        message = "Your Task #{} has been  successfully created".format(task.id)
        email_list = [request.user.email, user.email]
        send_email_task.delay(subject, message, email_list)
        return Response(status=status.HTTP_200_OK)

      response = {'error': 'Task or User not found'}
      return Response(response, status=status.HTTP_404_NOT_FOUND)

class TaskCommentView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CommentSerializer

    @swagger_auto_schema(operation_description="Get Comments for a Task", responses={200: "Success"})
    def get(self, request, id):
      comments = TaskComment.objects.filter(task_id=id).order_by('-created_at')
      serializer = self.serializer_class(comments, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="Add a Comment to a Task", responses={201: "Created", 400: "Bad Request"}, request_body=CommentSerializer)
    def post(self, request, id):
      task = get_object_or_None(Task, pk=id)
      if not task:
        return Response(status=status.HTTP_404_NOT_FOUND)

      serializer = TaskCommentSerializer(data=request.data)
      if serializer.is_valid():
        user = User.objects.get(id=request.user.id)
        taskComment = TaskComment.objects.create(user=user, task=task, comment=serializer.data['comment'])
        response_data = {'data': taskComment.comment}
        return Response(response_data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



