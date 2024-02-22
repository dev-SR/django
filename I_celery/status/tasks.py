from time import sleep
from celery import shared_task


@shared_task
def send_status(message=""):
    print("Sending status...")
    print(message)
    sleep(2)
    return "RUNNING"
