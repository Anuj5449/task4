from django.db import models

class Task(models.Model):
    TASK_STATUS = [
        ('pending','pending'),
        ('completed','completed'),
        ('in_progress','in_progress')
    ]
    task_id = models.IntegerField(primary_key = True,default = 2)
    task_name = models.CharField(max_length = 45)
    task_discription = models.TextField()
    task_status = models.CharField(max_length = 45, choices = TASK_STATUS )
    task_assigned_by = models.ForeignKey("customeapp.User", on_delete=models.CASCADE, related_name = 'user_task')
    task_assigned_to = models.ForeignKey("customeapp.User",on_delete=models.CASCADE, related_name = 'tasks')
    task_assigned_date = models.DateTimeField(auto_now_add = True)
    task_completed_date = models.DateTimeField(blank=True, null=True)
    task_deadline = models.DateTimeField(blank=True, null=True)
