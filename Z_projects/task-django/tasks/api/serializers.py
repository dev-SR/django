from rest_framework import serializers
from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'priority',
                  'is_complete', 'created_at', 'updated_at']

    # Add any additional validation or customization as needed
