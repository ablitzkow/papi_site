from django.shortcuts import render
from perguntas.models import Pergunta, Comentario , LikeBtn
from usuarios.models import Assinante

def score(user,user_id):
    email = user
    #Verifica o números de colaborações em PERGUNTAS efetuadas
    perguntas = Pergunta.objects.filter(user=user_id,publicada=True)
    id = set(pergunta.pk for pergunta in perguntas)
    qtd_perguntas = len(list(id))

    #Verifica o números de colaborações em COMENTÁRIOS
    comentarios = Comentario.objects.filter(email=email)
    ids = set(comentario.id_pergunta for comentario in comentarios)
    qtd_respostas = len(list(ids))


    #Verifica a qtd de curtidas nas RESPOSTAS
    print("IDS",ids)
    like = LikeBtn.objects.filter(id_pergunta__in = ids)
    likes = LikeBtn.objects.filter(id_pergunta__in = ids).count()
    print("asas", like)

    score_geral = qtd_perguntas*3+qtd_respostas*8+likes
    Assinante.objects.filter(email=user).update(score = score_geral)

    return score_geral , likes , qtd_perguntas , qtd_respostas