from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
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
        null=True
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