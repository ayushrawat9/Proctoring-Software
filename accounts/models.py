from email.policy import default
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django_base64field.fields import Base64Field
from django.utils.html import mark_safe


class UserProfile(AbstractUser):
    role = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)
    verifying_authority = models.CharField(max_length=50)
    user_image = Base64Field(max_length=900000, blank=True, null=False)

    def __str__(self):
        return f"{self.username}"

    def image_tag(self):
        return mark_safe('<img src="data:image/png;base64, %s" width="150" height="150" />' % (self.user_image))

    image_tag.short_description = 'Image'


