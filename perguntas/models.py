from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class Pergunta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pergunta = models.TextField(max_length=2000)
    intro_pergunta = models.TextField(max_length=150)
    comentario = models.TextField(blank=True,max_length=2000)
    assessor_email = models.CharField(max_length=150 , blank=True)
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
    revisor_email =  models.CharField(max_length=150 , blank=True)
    comentario_revisao = models.TextField(blank=True,max_length=2000)
    revisada = models.BooleanField(default=False)


class LikeBtn(models.Model):
    id_pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.BooleanField(default=False)


