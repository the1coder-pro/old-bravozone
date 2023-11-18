from django.utils import timezone
from django.db import models
from account.models import User

class Task(models.Model):
    TASK_STATUS_CHOICES = (
        ('completed', 'Completed'),
        ('in_process', 'In Process'),
        ('deletion', 'Deletion of the Task'),
    )

    name = models.CharField(max_length=255)
    content = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    points = models.IntegerField(choices=zip(range(1, 11), range(1, 11)))
    status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICES)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', 
                                    limit_choices_to={"is_superuser": False})


    def __str__(self):
        return self.name
    
    def update_status(self):
        if self.status != 'completed' and timezone.now() > self.end_time:
            self.status = 'completed'
            self.save()