from typing import Iterable
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage

from backgroundtasks.tasks import task_send_email


class BackgroundTaskEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages: Iterable[EmailMessage]) -> int:
        for message in email_messages:
            task_send_email(message)
        return len(list(email_messages))
