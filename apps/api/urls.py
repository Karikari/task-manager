from django.urls import path

from apps.api.views import *

app_name = 'api'

urlpatterns = [

  # GET , # POST
  path("tasks", TaskView.as_view(), name="tasks"),

  path("tasks/<uuid:id>", TaskDetailView.as_view(), name="task-details"), # GET, PUT, DELETE

  path("tasks/<uuid:task_id>/assign/<uuid:user_id>", AssignTaskView.as_view(), name="assign-task"), # POST

  path("tasks/<uuid:id>/comments", TaskCommentView.as_view(), name="task-comments"), # GET # POST
]