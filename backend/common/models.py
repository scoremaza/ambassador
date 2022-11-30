from datetime import timezone
import uuid
from django.db.models import BigAutoField
from django.db import models

class TimeStampedUUIDManager(models.Manager):
    """
    Manager definition for TimestampedUUIDManager
    Her we have the get_queryset that will return all the models 
    that haven't been deleted. 
    """

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class TimeStampedUUIDModel(models.Model):
    """
    Model definition for TimeStampUUIDModel
    Here we have a model with presets. This will help with not repeating 
    the same code over again in each model. From time stamp to softdelete and 
    harddelete. 
    """
    pkid        = BigAutoField(primary_key=True, editable=False, unique=True, help_text="")
    id          = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    deleted_at  = models.DateTimeField(null=True, blank=True, default=None)
    objects     = TimeStampedUUIDManager()
    all_objects = models.Manager()

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()
    
    def hard_delete(self):
        self.delete()

   
    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]
