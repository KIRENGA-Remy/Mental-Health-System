from django.contrib.auth.models import AbstractUser
from django.db import models

from db_connection import db

users_collection = db['Users']

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
