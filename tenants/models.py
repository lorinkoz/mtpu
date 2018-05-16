from django.db import models

from users.models import User


class RegisteredUser(User):
    
    registration_date = models.DateTimeField(auto_now_add=True)
    

class StaffUser(User):
    
    enrollment_date = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)


class SupportRole(models.Model):
    
    name = models.CharField(max_length=30)


class SupportStaffUser(StaffUser):
    
    role = models.ForeignKey(SupportRole, on_delete=models.PROTECT)


class PrimaryStaffUser(StaffUser):
    
    rank = models.PositiveIntegerField(default=1)
    team = models.ManyToManyField(SupportStaffUser, blank=True)