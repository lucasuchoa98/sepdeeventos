from django.db import models
from datetime import date, datetime

# Create your models here.

class Evento(models.Model):
    upload = models.FileField(upload_to='')