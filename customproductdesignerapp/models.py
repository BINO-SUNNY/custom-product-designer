# models.py
from django.contrib.auth.models import User
from django.db import models

# You don't need to create a custom model if you're just using the default User model.
# You can use the default User model for registration.


# Create your models here.
class logins(models.Model):
    email=models.EmailField(max_length=254)
    password=models.CharField(max_length=50)
    user_type=models.CharField(max_length=50)

class users(models.Model):
    name=models.CharField(max_length=254)
    phno=models.CharField(max_length=12)
    login=models.ForeignKey("logins", on_delete=models.CASCADE)
    def __str__(self):
        return self.name

