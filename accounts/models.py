from django.conf import settings
from django.db import models


class Profile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    national_code = models.CharField(
        max_length=10,
        unique=True,
        blank=True,
        null=True,
        default=None
    )

    birth_date = models.DateField(
        blank=True,
        null=True
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    province = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )


    def __str__(self):
        return self.user.username