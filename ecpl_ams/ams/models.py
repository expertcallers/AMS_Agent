from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class EcplCalander(models.Model):
    unique_id = models.CharField(max_length=150, null=True, blank=True)
    team = models.CharField(max_length=300)
    date = models.DateField()
    emp_name = models.CharField(max_length=300)
    emp_id = models.CharField(max_length=50)
    emp_desi = models.CharField(max_length=100)
    att_actual = models.CharField(max_length=50)
    approved_on = models.DateTimeField(null=True, blank=True)
    appoved_by = models.CharField(max_length=300, null=True, blank=True)
    rm1 = models.CharField(max_length=200, null=True, blank=True)
    rm2 = models.CharField(max_length=200, null=True, blank=True)
    rm3 = models.CharField(max_length=200, null=True, blank=True)
    rm1_id = models.CharField(max_length=30, null=True, blank=True)
    rm2_id = models.CharField(max_length=30, null=True, blank=True)
    rm3_id = models.CharField(max_length=30, null=True, blank=True)
    team_id = models.IntegerField(null=True, blank=True)


# Leave Balance - PL - SL +
class EmployeeLeaveBalance(models.Model):
    unique_id = models.CharField(max_length=150, null=True, blank=True)
    emp_id = models.CharField(max_length=10)
    emp_name = models.CharField(max_length=200)
    team = models.CharField(max_length=200)
    pl_balance = models.FloatField()
    sl_balance = models.FloatField()


# Leave apply - save - approval ++
class LeaveTable(models.Model):
    unique_id = models.CharField(max_length=150, null=True, blank=True)
    emp_name = models.CharField(max_length=200)
    emp_id = models.CharField(max_length=50)
    emp_desi = models.CharField(max_length=50)
    emp_process = models.CharField(max_length=50)
    leave_type = models.CharField(max_length=50)
    applied_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    no_days = models.IntegerField()
    agent_reason = models.TextField(null=True, blank=True)
    tl_approval = models.BooleanField(default=False)
    tl_status = models.CharField(max_length=50, null=True, blank=True)
    tl_reason = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, null=True)
    manager_approval = models.BooleanField(default=False)
    manager_reason = models.TextField(null=True, blank=True)
    manager_status = models.CharField(max_length=50, null=True, blank=True)
    emp_rm1 = models.CharField(max_length=200)
    emp_rm2 = models.CharField(max_length=200)
    emp_rm3 = models.CharField(max_length=200)
    emp_rm1_id = models.CharField(max_length=50)
    emp_rm2_id = models.CharField(max_length=50)
    emp_rm3_id = models.CharField(max_length=50)
    escalation = models.BooleanField(default=False)
    escalation_reason = models.TextField(null=True, blank=True)
    proof = models.FileField(null=True, blank=True,upload_to='Uploads/SL_Proof')


class leaveHistory(models.Model):
    unique_id = models.CharField(max_length=150, null=True, blank=True)
    emp_id = models.CharField(max_length=30)
    date = models.DateField()
    leave_type = models.CharField(max_length=30)
    transaction = models.CharField(max_length=300)
    no_days = models.FloatField()
    total = models.FloatField()
