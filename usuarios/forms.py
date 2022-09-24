import email
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from perguntas.models import Comentario, Pergunta, Revisao , LikeBtn
from usuarios.models import Assinante , Registro_Email
from django import forms
from captcha.fields import ReCaptchaField


class ReCaptcha(forms.Form):
    Captcha = ReCaptchaField()

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


def form_pergunta(request):
    from perguntas.met_pergunta import remove_emojis, nick_user
    from usuarios.score import score
    import shortuuid
    from usuarios.forms import ReCaptcha
    if request.method == 'POST':
        form = ReCaptcha(request.POST)
        if form.is_valid():
            user = get_object_or_404(User, pk=request.user.id)
            pergunta = request.POST['pergunta']
            print(request.POST['pergunta'])
            faculdade = request.POST['faculdade']
            disciplina = request.POST['disciplina']
            pergunta = remove_emojis(pergunta)
            intro_pergunta = pergunta[0:150]
            nick = nick_user(user)
            print(intro_pergunta)
            id_url = shortuuid.uuid() 
            pergunta_feita = Pergunta.objects.create(id_url=id_url, user=user, email=user.email,nick = nick , pergunta=pergunta, intro_pergunta = intro_pergunta , disciplina=disciplina, faculdade=faculdade)
            pergunta_feita.save()
            contexto = {}
            if Assinante.objects.filter(email=request.user.email, mensalidade = True).exists():
                assinante = get_object_or_404(Assinante, email = request.user.email)
                score(request.user.email,request.user.id)
                contexto = {
                    'dados_assinante':assinante,
                }
            print('Pergunta salva com sucesso')
            return redirect('minhas_perguntas')
        else:
            form = ReCaptcha()
            return render(request, 'usuarios/form_pergunta.html',{'form':form,'erro':'Captcha Inválido'})

    else:
        form = ReCaptcha()
        return render(request, 'usuarios/form_pergunta.html',{'form':form})

def cadastro(request):
    from random import randint
    from datetime import datetime
    from django.core.mail import send_mail
    if request.method == 'POST':
        form = ReCaptcha(request.POST)
        if form.is_valid():
            email = request.POST['email'].lower()
            #verifica se o email já está cadastrado:
            if not User.objects.filter(email=email).exists():
                code = randint(100000,999999)
                date = datetime.now()
                print("code:",code)

                if Registro_Email.objects.filter(email_register=email).exists():
                    Registro_Email.objects.filter(email_register=email).update(code_sent=code,data_code=date)
                else:
                    Registro_Email.objects.create(email_register=email,code_sent=code,data_code=date)

                contexto = {
                    'email' : email,
                        }
                send_mail('Código de Verificação - '+str(code), 'Seu código é '+str(code), 'contato@papiron.com.br',
                [email], fail_silently=False)

                return render(request,'usuarios/form/form_email_code.html',contexto)
            else:
                #Cria uma instância vazia devido a tentativa de cadastrar um email já constante na BD
                form = ReCaptcha()
                contexto = {
                    'email' : email,
                    'erro_email' : 'E-mail já cadastrado',
                    'form': form,}

        else:
            #Cria uma instância vazia devido Recaptcha Inválido
            form = ReCaptcha()
            contexto = {
                'erro_captcha':'Recapatcha Inválido',
                'form': form,}

    else:
        #Cria uma instância vazia pela primeira requisição GET
        form = ReCaptcha()
        contexto = {
                'form': form,}
    return render(request, 'usuarios/form/cadastro.html',contexto)



def form_email_code(request):
    from datetime import datetime
    if request.method == 'POST':
        email = request.POST['email_register']
        code = request.POST['code']
        code_save = get_object_or_404(Registro_Email,email_register=email)

        #verifica a expiração do código, válido até o final do dia
        date = code_save.data_code
        date_now = datetime.now().date()

        if str(code) == str(code_save.code_sent) and date==date_now:
            print("Código OK") 
            contexto = {
                'email' : email,
                 }
            return render(request,'usuarios/form/dados_cadastro.html',contexto)
        
        #caso o código esteja expirado
        elif date!=date_now:
            print("Código expirado", code , code_save.code_sent)
            contexto = {
                'email' : email,
                'erro': 'Código expirado'
                }
            return render(request,'usuarios/form_email_code.html',contexto)
        
        else:
            print("Código ERRADO", code , code_save.code_sent)
            contexto = {
                'email' : email,
                'erro': 'Código incorreto'
                }
            return render(request,'usuarios/form_email_code.html',contexto)
        
    else:
        return redirect('cadastro')


def captcha(request):
    if request.method == 'POST':
        form = ReCaptcha(request.POST)
        if form.is_valid():
            email = request.POST['email']
            print("deu certo",email)
            contexto = {
                'form':form}
            
            return render(request,'captcha.html',contexto)
        else:
            print("Não clicou")
    else:
            form = ReCaptcha()
    contexto = {
        'form':form
    }
    return render(request,'captcha.html',contexto)