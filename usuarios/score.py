import email
from django.shortcuts import render , get_object_or_404
from perguntas.models import Pergunta, Comentario , LikeBtn
from usuarios.models import Assinante , Stat_WhatsApp


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

def eventos_whatsapp(user):
    #Verifica o números de colaborações em PERGUNTAS efetuadas
    print("user",user)
    assinante = get_object_or_404(Assinante,email=user)
    cliques = Stat_WhatsApp.objects.filter(assinante_id= assinante.pk)
    id = set(clique.id for clique in cliques)
    print(id)
    qtd_eventos = len(list(id))
    return qtd_eventos