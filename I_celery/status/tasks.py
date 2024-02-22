import time
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from time import sleep
from celery import shared_task


@shared_task
def send_status(message=""):
    print("Sending status...")
    print(message)
    sleep(2)
    return "RUNNING"


@shared_task
def send_status_periodically(num_iterations):
    channel_layer = get_channel_layer()
    statuses = ['RUNNING', 'FINISHED']
    iteration = 0

    while iteration < num_iterations:
        status_index = iteration % 2  # Odd iteration will be 1, even will be 0
        status = statuses[status_index]
        async_to_sync(channel_layer.group_send)(
            'status',
            {
                'type': 'send_status',
                'status': status
            }
        )
        iteration += 1
        time.sleep(5)  # Sleep for 5 seconds before sending the next status
