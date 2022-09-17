from django.shortcuts import render
from perguntas.models import Pergunta, Revisao , LikeBtn
from usuarios.models import Assinante

def score(user,user_id):
    email = user
    #Verifica o números de colaborações em PERGUTNAS efetuadas
    print("XXXXXX1",user)
    perguntas = Pergunta.objects.order_by('-date_pergunta').filter(user=user_id)
    print("XXXXXX2",perguntas)
    id = set(pergunta.pk for pergunta in perguntas)
    print("XXXXXX3",id)
    qtd_perguntas = len(list(id))
    print("XXXXXX4",qtd_perguntas)
    
    #Verifica o números de colaborações em RESPOSTAS
    perguntas = Pergunta.objects.order_by('-date_pergunta').filter(email_comentario=email)
    ids = set(pergunta.id for pergunta in perguntas)
    qtd_respostas = len(list(ids))
    print("XXXXXX4",qtd_respostas,ids)

    #Verifica a qtd de curtidas nas RESPOSTAS
    likes = LikeBtn.objects.filter(id_pergunta__in = ids).count()
    print("asas",LikeBtn.objects.filter(id_pergunta = '20'))

    score_geral = qtd_perguntas*3+qtd_respostas*8+likes

    Assinante.objects.filter(email=user).update(score = score_geral)

    return score_geral , likes , qtd_perguntas , qtd_respostas