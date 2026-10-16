from django.db import models

#Django automatically creates a primary key field that autoincrements
#passwords currently not hashed
class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)

