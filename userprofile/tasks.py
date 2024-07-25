from celery import shared_task

from user_microservice.celery import app


@shared_task
def send_user_profile(data):
    app.send_task('authapp.tasks.handle_user_profile', args=[data])
