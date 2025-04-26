import uuid

from django.db import models


class ApiIdField(models.UUIDField):
    def __init__(self, *args, **kwargs):
        kwargs["default"] = uuid.uuid4
        kwargs["editable"] = False
        kwargs["unique"] = True
        kwargs["help_text"] = "Unique identifier for the object in the API"
        super().__init__(*args, **kwargs)


class BaseModel(models.Model):
    api_id = ApiIdField()
    added_at = models.DateTimeField(
        auto_now_add=True, help_text="Timestamp when the object was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Timestamp when the object was last updated"
    )

    class Meta:
        abstract = True
        ordering = ["-added_at"]
