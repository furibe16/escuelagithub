from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class perfil(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	nombre = models.CharField(max_length=100, blank=False, default='')
	avatar = models.ImageField(upload_to='perfiles',blank=True, null=True)
	biografia = models.TextField(null=True, blank=True)
	recibemails = models.BooleanField(default=False)
	alumno = models.BooleanField(default=False)
	profesor = models.BooleanField(default=False)
	sexo = models.CharField(max_length=1, default='F')
	nacimiento = models.DateField(blank=True, null=True)


