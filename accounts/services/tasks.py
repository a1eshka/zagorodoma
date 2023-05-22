from celery import shared_task

from .email import send_activate_email_message, send_publish_post_message


@shared_task
def send_activate_email_message_task(user_id):
    """
    1. Задача обрабатывается в представлении: UserRegisterView
    2. Отправка письма подтверждения осуществляется через функцию: send_activate_email_message
    """
    return send_activate_email_message(user_id)
@shared_task
def send_publish_post_message_task(author,post_url):
    """
    1. Задача обрабатывается в представлении: UserRegisterView
    2. Отправка письма подтверждения осуществляется через функцию: send_activate_email_message
    """
    return send_publish_post_message(author, post_url)