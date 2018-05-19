from django.conf import settings
from django.db import models
from django.utils.dateformat import format as format_date

from users.models import User


class RegisteredUser(User):
    
    registration_date = models.DateTimeField(auto_now_add=True)
    
    @property
    def stats(self):
        return [
            ('registered on', format_date(self.registration_date, settings.DATETIME_FORMAT)),
        ]
    

class StaffUser(User):
    
    enrollment_date = models.DateTimeField(auto_now_add=True)
    
    @property
    def stats(self):
        return [
            ('enrolled on', format_date(self.enrollment_date, settings.DATETIME_FORMAT)),
        ]


class SupportStaffUser(StaffUser):
    
    ROLES = (
        (1, 'assistant'),
        (2, 'bodyguard'),
        (3, 'billing manager'),
        (4, 'mentor'),
    )
    
    role = models.PositiveIntegerField(choices=ROLES, default=1)
    
    @property
    def stats(self):
        return super().stats + [
            ('role', self.get_role_display()),
        ]


class PrimaryStaffUser(StaffUser):
    
    rank = models.PositiveIntegerField(default=1)
    team = models.ManyToManyField(SupportStaffUser, blank=True)
    
    @property
    def stats(self):
        return super().stats + [
            ('rank', self.rank),
            ('team', '\r\n'.join([x.display_name for x in self.team.all()])),
        ]