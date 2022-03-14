
# Create your models here.
# using django user model, don't need to create own

# Account related models/functionality

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # Any extra fields would go here
    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return self.email
