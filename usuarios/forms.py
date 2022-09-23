import email
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from perguntas.models import Comentario, Pergunta, Revisao , LikeBtn
from usuarios.models import Assinante , Registro_Email

def random_id(length):
    import random
    number = '0123456789'
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    id = ''
    for i in range(0,length):
        id += random.choice(number+alpha)
    return id

def incluir_assinante(request):
    return render(request, 'usuarios/form/incluir_assinante.html')


def form_incluir_assinante(request):
    from perguntas.met_pergunta import remove_emojis, nick_user

    email = request.POST['email']
    cpf = request.POST['cpf']
    if User.objects.filter(email = email).exists():
        if not Assinante.objects.filter(email = email).exists():
            user = get_object_or_404(User, email=email)
            id_perfil = random_id(5)
            nick = nick_user(user)
            Assinante.objects.create(assinante_id=user.id, id_perfil = id_perfil, email=email, CPF = cpf ,nome = user.first_name , sobrenome = user.last_name , nick = nick )
            contexto = {
                'user':user
            }
            print(user.email, user.first_name, id_perfil)
            return render(request, 'usuarios/form/incluir_finalizado.html',contexto)
        else:
            contexto = {
            
            'erro': 'Este usuário já é cadastrado:',
            'email': email
        }
            print(contexto)
            return render(request, 'usuarios/form/incluir_assinante.html',contexto)

    else:
        contexto = {
            
            'erro': 'Este usuário não ecxiste:',
            'email': email
        }
        print(contexto)
        return render(request, 'usuarios/form/incluir_assinante.html',contexto)