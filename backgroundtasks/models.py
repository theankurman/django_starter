from django.db import models


# Create your models here.
class KV(models.Model):
    """Model definition for KV."""

    queue = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    value = models.BinaryField()

    class Meta:
        """Meta definition for KV."""

        verbose_name = "KV"
        verbose_name_plural = "KVs"
        constraints = [
            models.UniqueConstraint(
                fields=["queue", "key"],
                name="unique_kv_queue_key",
            ),
        ]


class Schedule(models.Model):
    """Model definition for Schedule."""

    queue = models.CharField(max_length=255)
    data = models.BinaryField()
    timestamp = models.DateTimeField()

    class Meta:
        """Meta definition for Schedule."""

        verbose_name = "Schedule"
        verbose_name_plural = "Schedules"
        indexes = [
            models.Index(
                fields=["queue", "timestamp"],
                name="idx_schedule_queue_timestamp",
            )
        ]
        ordering = ["timestamp"]


class Task(models.Model):
    """Model definition for Task."""

    queue = models.CharField(max_length=255)
    data = models.BinaryField()
    priority = models.FloatField(default=0.0)

    class Meta:
        """Meta definition for Task."""

        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        indexes = [
            models.Index(
                fields=["priority", "id"],
                name="idx_task_priority_id",
            )
        ]
        ordering = [
            "-priority",
            "id",
        ]
