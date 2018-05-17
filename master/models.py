from django.db import models
from django.conf import settings
from django.db.models import Case, When, Value, Max

from django_tenants.models import TenantMixin, DomainMixin

from users.models import User


class TenantManager(models.Manager):

    def get_queryset(self):
        qs = super(TenantManager, self).get_queryset()
        core_case = Case(
            When(schema_name='public', then=True),
            default=Value(False),
            output_field=models.BooleanField()
        )
        qs = qs.annotate(is_core=core_case)
        qs = qs.annotate(domain=Max('domains__domain'))
        return qs


class Tenant(TenantMixin):

    auto_drop_schema = True
    objects = TenantManager()

    def __str__(self):
        return self.schema_name


class Domain(DomainMixin):

    class Meta:
        ordering = ('is_primary',)

    def __str__(self):
        return self.domain


class MasterUser(User):
    pass
    