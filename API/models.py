from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email=models.EmailField()
    access_token=models.CharField(max_length=200)
    token = models.CharField(max_length=200)
    token_last_update=models.DateField()
    first_login=models.DateField(auto_now_add=True)

