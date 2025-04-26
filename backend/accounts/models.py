from core.models import ApiIdField, BaseModel
from django.contrib.auth.models import AbstractUser
from django.db import models


class Contact(BaseModel):
    phone_number = models.CharField(max_length=15)
    postal_code = models.CharField(max_length=10)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id} - {self.phone_number} - {self.postal_code} - {self.city} - {self.state} - {self.country}"


class Company(BaseModel):
    name = models.CharField(max_length=255)
    contact = models.OneToOneField(
        Contact,
        on_delete=models.SET_NULL,
        related_name="company",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.id} - {self.name}"


class User(AbstractUser):
    api_id = ApiIdField()
    contact = models.OneToOneField(
        Contact, on_delete=models.SET_NULL, related_name="user", null=True, blank=True
    )
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, related_name="users", null=True, blank=True
    )

    def __str__(self):
        return f"{self.id} - {self.username}"
