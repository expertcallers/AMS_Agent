from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    emp_id = models.CharField(max_length=100)
    emp_name = models.CharField(max_length=200)
    emp_desi = models.CharField(max_length=200)
    emp_rm1 = models.CharField(max_length=200)
    emp_rm1_id = models.CharField(max_length=30)
    emp_rm2 = models.CharField(max_length=200)
    emp_rm2_id = models.CharField(max_length=30)
    emp_rm3 = models.CharField(max_length=200)
    emp_rm3_id = models.CharField(max_length=30)
    emp_process = models.CharField(max_length=200)
    emp_process_id = models.CharField(max_length=10)
    pc = models.BooleanField(default=False)
    img = models.ImageField(upload_to='users/',default="users/default.png")
    doj = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    on_id = models.IntegerField(null=True, blank=True)
    agent_status = models.CharField(max_length=30, default='Active')

    def __str__(self):
        return self.emp_name
