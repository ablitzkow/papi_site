from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Pergunta(models.Model):
    #dados do usuario que faz a pergunta
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email_pergunta = email_comentario = models.CharField(max_length=200)
    pergunta = models.TextField(max_length=2500)
    intro_pergunta = models.TextField(max_length=150)
    #dados do assessor que responde
    comentario = models.TextField(blank=True,max_length=2500)
    email_comentario = models.CharField(max_length=200, blank=True)
    disciplina = models.CharField(max_length=150)
    faculdade = models.CharField(max_length=150)
    date_pergunta = models.DateTimeField(default=datetime.now, blank=True)
    publicada = models.BooleanField(default=False)
    revisao_solicitada = models.BooleanField(default=False)
    revisao_qtd = models.IntegerField(default=0)
    def __str__(self):
        id_str = str(self.id)
        return id_str

class Revisao(models.Model):
    id_pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    email_revisor =  models.CharField(max_length=200 , blank=True)
    comentario_revisao = models.TextField(blank=True,max_length=2000)
    revisada = models.BooleanField(default=False)

class LikeBtn(models.Model):
    id_pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.BooleanField(default=False)



