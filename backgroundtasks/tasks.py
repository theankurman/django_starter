from django.conf import settings
from django.core import mail
from huey.contrib.djhuey import task


@task()
def task_send_email(message: mail.EmailMessage):
    email_backend = getattr(
        settings,
        "BACKGROUND_TASK_EMAIL_BACKEND",
        "django.core.mail.backends.smtp.EmailBackend",
    )
    connection = mail.get_connection(email_backend)
    connection.send_messages([message])
