from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Assinante(models.Model):
    assinante = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=200)
    nome = models.CharField(max_length=200)
    sobrenome = models.CharField(max_length=200)
    mensalidade = models.BooleanField(default=False)
    CPF = models.CharField(max_length=200,unique=True)
    instagram = models.CharField(max_length=200,blank=True)
    whatsapp_ddd = models.CharField(max_length=2,blank=True)
    whatsapp =  models.CharField(max_length=25,blank=True)
    linkedIn =  models.CharField(max_length=200,blank=True)
    facebook =  models.CharField(max_length=200,blank=True)
    descricao = models.CharField(max_length=1000,blank=True)
    score = models.IntegerField(blank=True,default=0)
    foto = models.ImageField(upload_to='papiron/static/media/usuarios/', blank=True,default='papiron/static/media/usuarios/no-image.png')
    def __str__(self):
        return self.email

class Registro_Email(models.Model):
    email_register =  models.CharField(max_length=200)
    code_sent = models.IntegerField()
    data_code = models.DateField()
    approve_code = models.BooleanField(default=False)
    def __str__(self):
        return self.email_register