from django.db import models
from django.contrib.auth.models import User

class Assinante(models.Model):
    assinante = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=200)
    # nick_assinante = models.CharField(max_length=200)
    nome = models.CharField(max_length=200)
    sobrenome = models.CharField(max_length=200)
    mensalidade = models.BooleanField(default=False)
    CPF = models.CharField(max_length=200)
    instagram = models.CharField(max_length=200,blank=True)
    whatsapp_ddi = models.CharField(max_length=3,default='+55')
    whatsapp_ddd = models.CharField(max_length=3,blank=True)
    whatsapp =  models.CharField(max_length=25,blank=True)
    linkedIn =  models.CharField(max_length=300,blank=True)
    facebook =  models.CharField(max_length=300,blank=True)
    youtube =  models.CharField(max_length=300,blank=True)
    homepage =  models.CharField(max_length=300,blank=True)
    descricao = models.CharField(max_length=2500,blank=True)
    resumo = models.CharField(max_length=250,blank=True)
    plano = models.CharField(max_length=300,blank=True)
    score = models.IntegerField(blank=True,default=0)
    foto = models.ImageField(upload_to='media/usuarios/', blank=True,default='/media/usuarios/no-image.png')
    def __str__(self):
        return self.assinante

class Registro_Email(models.Model):
    email_register =  models.CharField(max_length=200)
    code_sent = models.IntegerField()
    data_code = models.DateField()
    approve_code = models.BooleanField(default=False)
    def __str__(self):
        return self.email_register