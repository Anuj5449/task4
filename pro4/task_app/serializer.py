from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    task_assigned_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    task_deadline = serializers.DateTimeField(format="%d/%m/%Y %H:%M",input_formats=['%d/%m/%Y %H:%M'])
    task_assigned_date = serializers.DateTimeField(format="%d/%m/%Y %H:%M",read_only=True)
    task_completed_date = serializers.DateTimeField(format="%d/%m/%Y %H:%M",input_formats=['%d/%m/%Y %H:%M'])
    class Meta:
        model = Task
        fields  = '__all__'