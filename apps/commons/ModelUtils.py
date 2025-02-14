import uuid

from django.db import models


class CoreModel(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    abstract = True
    verbose_name = 'CoreModel'
    verbose_name_plural = 'CoreModels'


def get_object_or_None(model_class, pk):
  try:
    result = model_class.objects.get(pk=pk)
  except model_class.DoesNotExist:
    result = None
  return result

def get_user_by_email(model_class, email):
  try:
    result = model_class.objects.get(email=email)
  except model_class.DoesNotExist:
    result = None
  return result