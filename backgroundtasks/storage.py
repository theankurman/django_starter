from datetime import UTC
from django.db import close_old_connections, transaction
from huey.storage import BaseStorage
from huey.storage import EmptyData
from huey import Huey


class DjangoOrmStorage(BaseStorage):
    """
    Huey storage-layer using the Django ORM.
    """

    blocking = False  # Does dequeue() block until ready, or should we poll?
    priority = True

    def __init__(self, name="huey", **storage_kwargs):
        super().__init__(name, **storage_kwargs)

    def _tasks(self):
        from .models import Task

        return Task.objects.filter(queue=self.name)

    def _kv(self):
        from .models import KV

        return KV.objects.filter(queue=self.name)

    def _schedule(self):
        from .models import Schedule

        return Schedule.objects.filter(queue=self.name)

    def close(self):
        close_old_connections()

    def enqueue(self, data, priority=None):
        self._tasks().create(queue=self.name, data=data, priority=priority or 0)

    @transaction.atomic
    def dequeue(self):
        task = self._tasks().select_for_update(skip_locked=True).first()
        if not task:
            return None
        data = task.data
        task.delete()

        return data

    def queue_size(self):
        return self._tasks().count()

    def enqueued_items(self, limit=None):
        qs = self._tasks()
        if limit is not None:
            qs = qs[:limit]
        return [t.data for t in qs]

    def flush_queue(self):
        self._tasks().delete()

    def add_to_schedule(self, data, ts):
        self._schedule().create(
            queue=self.name, data=data, timestamp=ts.astimezone(UTC)
        )

    @transaction.atomic
    def read_schedule(self, ts):
        qs = (
            self._schedule()
            .filter(timestamp__lte=ts.astimezone(UTC))
            .select_for_update()
        )
        data = [s.data for s in qs]
        qs.delete()
        return data

    def schedule_size(self):
        return self._schedule().count()

    def scheduled_items(self, limit=None):
        qs = self._schedule()
        if limit is not None:
            qs = qs[:limit]
        return [s.data for s in qs]

    def flush_schedule(self):
        self._schedule().delete()

    def put_data(self, key, value, is_result=False):
        self._kv().update_or_create(
            queue=self.name,
            key=key,
            defaults={"value": value},
        )

    def peek_data(self, key):
        kv = self._kv().filter(key=key).first()
        if not kv:
            return EmptyData
        return kv.value

    @transaction.atomic
    def pop_data(self, key):
        kv = self._kv().filter(key=key).first()
        if not kv:
            return EmptyData
        data = kv.value
        kv.delete()
        return data

    def delete_data(self, key):
        num_deleted, _ = self._kv().filter(key=key).delete()
        return bool(num_deleted)

    def has_data_for_key(self, key):
        return self._kv().filter(key=key).exists()

    @transaction.atomic
    def put_if_empty(self, key, value):
        if self.has_data_for_key(key):
            return False
        self.put_data(key, value)
        return True

    def result_store_size(self):
        return self._kv().count()

    def result_items(self):
        qs = self._kv()
        return {k: v for k, v in qs.values_list("key", "value")}

    def flush_results(self):
        self._kv().delete()

    def flush_all(self):
        self.flush_queue()
        self.flush_schedule()
        self.flush_results()


class DjangoOrmHuey(Huey):
    storage_class = DjangoOrmStorage
