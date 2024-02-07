import os
from pathlib import Path
from django.contrib.auth.models import User
from tasks.models import Task, Photo
from faker import Faker
import random
from django.utils import timezone


def create_fake_task(user):
    fake = Faker()
    title = fake.sentence()
    description = fake.paragraph()
    due_date = fake.future_datetime(end_date='+10d', tzinfo=timezone.get_current_timezone())
    priority = random.choice(['low', 'medium', 'high'])
    is_complete = random.choice([True, False])
    created_at = fake.past_datetime(start_date='-10d', tzinfo=timezone.get_current_timezone())

    task = Task.objects.create(
        title=title,
        description=description,
        due_date=due_date,
        priority=priority,
        is_complete=is_complete,
        owner=user,
    )
    task.created_at = created_at
    task.save()

    ROOT_DIR = Path(os.getcwd())
    uploads = ROOT_DIR / "uploads" / "task_photos"
    images = list(uploads.glob("*"))

    # Add random number of photos to the task
    for i in range(random.randint(1, len(images))):
        create_fake_photo(task, images[i])


def create_fake_photo(task, image_path):
    fake = Faker()
    caption = fake.word()
    image_name = f"task_photos/{image_path.name}"
    Photo.objects.create(
        caption=caption,
        image=image_name,
        task=task,
    )


def run():
    Photo.objects.all().delete()
    Task.objects.all().delete()
    users = User.objects.all()
    for user in users:
        # Create n tasks for each user
        print(f"> Creating tasks for user {user.username}")
        for i in range(30):  # You can adjust the number of tasks to create
            print(f"    > Task {i}")
            create_fake_task(user)
