from django.db import models

from apps.commons.ModelUtils import CoreModel

# Create your models here.
STATUS_CHOICES = {("Pending", "Pending"), ("Progress","Progress"), ("Completed","Completed"), ("Cancelled", "Cancelled")}

class Task(CoreModel):
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    due_date = models.DateField(blank=True, null=True)
    assign_to = models.ForeignKey(to='auths.User', on_delete=models.CASCADE, related_name='+', default='')

    class Meta:
      verbose_name = 'Task'
      verbose_name_plural = 'Tasks'

    def __str__(self):
        return self.title

class TaskComment(CoreModel):
    task = models.ForeignKey(to=Task, on_delete=models.CASCADE, related_name='+', default='')
    user = models.ForeignKey(to='auths.User', on_delete=models.CASCADE, related_name='+', default='')
    comment = models.TextField(max_length=255, blank=True)

    class Meta:
      verbose_name = 'TaskComment'
      verbose_name_plural = 'TaskComments'

    def __str__(self):
        return self.comment

