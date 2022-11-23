import email
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from perguntas.met_pergunta import nick_user
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
            pergunta = request.POST['pergunta'][:24990]
            if len(pergunta)>=299:
                intro_pergunta = pergunta[0:299].replace("<b>","").replace("</b>","").replace("<i>","").replace("<br>","").replace("<p>","").replace("</p>","").replace("<hr>","")+'...'
            else:
                intro_pergunta = pergunta[0:299].replace("<b>","").replace("</b>","").replace("<i>","").replace("<br>","").replace("<p>","").replace("</p>","").replace("<hr>","")
            faculdade = request.POST['faculdade']
            disciplina = request.POST['disciplina']
            pergunta = remove_emojis(pergunta)
            nick = nick_user(user)
            id_url = shortuuid.uuid() 
            contexto = {}
            if Assinante.objects.filter(email=request.user.email, mensalidade = True).exists():
                assinante = get_object_or_404(Assinante, email = request.user.email)
                score(request.user.email,request.user.id)
                pergunta_feita = Pergunta.objects.create(id_url=id_url, user=user, email=user.email,nick = nick , pergunta=pergunta, intro_pergunta = intro_pergunta , disciplina=disciplina, faculdade=faculdade,publicada=True)
                pergunta_feita.save()
                contexto = {
                    'assinante':assinante,
                }
            else:
                pergunta_feita = Pergunta.objects.create(id_url=id_url, user=user, email=user.email,nick = nick , pergunta=pergunta, intro_pergunta = intro_pergunta , disciplina=disciplina, faculdade=faculdade)
                pergunta_feita.save()
            
            
            return redirect("minhas_perguntas")

        else:
            pre_pergunta = request.POST['pergunta']
            form = ReCaptcha()
            return render(request, 'usuarios/form_pergunta.html',{'pre_pergunta':pre_pergunta,'form':form,'erro':'Captcha Inválido'})

    else:
        form = ReCaptcha()
        return render(request, 'usuarios/form_pergunta.html',{'form':form})

def form_comentar(request):
    from usuarios.forms import ReCaptcha
    from usuarios.score import score
    if request.method == 'POST':
        # Dados do POST do comentário
        email_user = request.user.email
        recaptcha= ReCaptcha(request.POST)
        comentario = request.POST['comentario']
        id_pergunta = request.POST['id_pergunta']
        pergunta = get_object_or_404(Pergunta, id = id_pergunta)
        assinante = get_object_or_404(Assinante,email=email_user)

        if recaptcha.is_valid():
            nick = nick_user(request.user)
            Comentario.objects.create(id_pergunta_id=id_pergunta, comentario=comentario, email=email_user,nick=nick)
            Pergunta.objects.filter(id=id_pergunta).update(comentario_check = True)
            assinante = get_object_or_404(Assinante,email=email_user)
            score(email_user,request.user.id)
            print("ok")
        else:
            # REFAZ POR CAUSA DO RECAPTCHA INVÁLIDO
            from perguntas.met_pergunta import usuario_logado_assinante
            recaptcha= ReCaptcha()
            print("not ok")

        ### Realimentando com os dados da pergunta
        pergunta = get_object_or_404(Pergunta, id = id_pergunta)
        likes_count = LikeBtn.objects.filter(id_pergunta = pergunta.pk).count() # Qtd de Likes
        
        # Formata pelo tamanho da pergunta
        if len(pergunta.pergunta)>=1750:
            n = pergunta.pergunta[700:].find("\n")
            pergunta_inicio = pergunta.pergunta[:700+n].replace('\n','<br>')
            pergunta_fim = pergunta.pergunta[700+n+1:].replace('\n','<br>')
            pergunta_texto = None
        else:
            pergunta_texto = pergunta.pergunta.replace('\n','<br>')
            pergunta_inicio = None
            pergunta_fim = None

        contexto = {
        'assinante': assinante,
        'title' : 'Papiron - '+pergunta.faculdade+' - '+pergunta.intro_pergunta,
        'pergunta'  : pergunta,
        'comentario': comentario,
        'comentario_texto':comentario.replace('\n','<br>'),
        'pergunta_texto':pergunta_texto,
        'pergunta_inicio':pergunta_inicio,
        'pergunta_fim':pergunta_fim,
        'usuario_logado_assinante': 'é assinante',
        'my_like' : False,
        'likes_count':0,
        'recaptcha' : recaptcha ,
        'erro_recaptcha_comentario':'Recaptcha Inválido',
        'pre_comentario':comentario
        }
        return render(request,'perguntas/pergunta.html', contexto )

    else:
        return render(request, 'usuarios/form_pergunta.html')


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