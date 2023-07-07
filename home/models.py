from django.db import models
from zerowaste.models import AuthUser

# Create your models here.
class student(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)

    class Meta:
        managed=True
        db_table = 'student'

class TaskStudent(models.Model):
    username = models.ForeignKey(student, on_delete=models.CASCADE, db_column='username')
    task_name = models.CharField(max_length=100)
    task_status = models.CharField(max_length=100)
    task_start_date = models.DateField()
    task_completion_date = models.DateField(null=True)

    class Meta:
        db_table = 'tasks'
        # When i select the username and add task that data should be stored in 

class LoginUsers(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    class Meta:
        db_table = 'admin_login'

class tasks_zerowaste(models.Model):
    zerowaste_user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=100)
    task_status = models.CharField(max_length=20)
    task_start_date = models.DateField()
    task_completion_date = models.DateField()
    username = models.CharField(max_length=50)

    class Meta:
        db_table = 'tasks_zerowaste'
        