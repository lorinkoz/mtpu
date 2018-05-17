from django.db import models

from users.models import User


class RegisteredUser(User):
    
    registration_date = models.DateTimeField(auto_now_add=True)
    

class StaffUser(User):
    
    enrollment_date = models.DateTimeField(auto_now_add=True)


class SupportStaffUser(StaffUser):
    
    ROLES = (
        (1, 'assistant'),
        (2, 'bodyguard'),
        (3, 'billing manager'),
        (4, 'mentor'),
    )
    
    role = models.PositiveIntegerField(choices=ROLES, default=1)


class PrimaryStaffUser(StaffUser):
    
    rank = models.PositiveIntegerField(default=1)
    team = models.ManyToManyField(SupportStaffUser, blank=True)