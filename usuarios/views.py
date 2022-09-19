from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from perguntas.met_pergunta import nick
from perguntas.models import Pergunta, Revisao , LikeBtn
from usuarios.models import Assinante , Registro_Email
from usuarios.score import score


def cadastro(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email_register'].lower()
        password = request.POST['password']
        password2 = request.POST['password2']

        # verificando se o usuário já está cadastrado
        if User.objects.filter(email=email).exists():
            erro_a_exibir = {
                'erro' : 'Email já cadastrado'
            }
            return render(request,'usuarios/cadastro.html', erro_a_exibir)
        
        #verifica se as senhas são iguais
        elif password != password2:
            contexto = {
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'erro' : 'Senhas não coincidem'
            }
            print("Senhas não coincidem")
            return render(request,'usuarios/cadastro.html', contexto)
            
        #verifica a segurança da senha
        else:
            #verifica se a senha possui no mínimo 8 caracteres
            if len(password)<8:
                contexto = {
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'erro' : 'Senha insegura, insira no mínimo 8 caracteres',
                }
                print('senha insegura')
                return render(request,'usuarios/cadastro.html', contexto)
            #verifica se possuí 1 minúscula, 1 maiúscula e 1 número
            lower , upper , number = False , False , False
            for letra in password:
                if letra.islower():
                    lower = True
                    print("lower ok")
                    break

            for letra in password:
                if letra.isupper():
                    upper = True
                    print("upper ok")
                    break

            for letra in password:
                if letra.isdigit():
                    number = True
                    print("number ok")
                    break
                
            if lower and upper and number:
                contexto = {
                    'email': email,
                }
                print("FN2", first_name, last_name)
                user = User.objects.create_user(username=email, email=email, password=password ,first_name=first_name,last_name=last_name)
                Registro_Email.objects.filter(email_register=email).delete()
                user.save()
                return render(request,'usuarios/login.html',contexto)

            else:
                contexto = {
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'erro' : 'Senha insegura, insira no mínimo: 1 letra minúscula, 1 maiúscula e 1 número',
                }
                print('senha insegura')
                return render(request,'usuarios/cadastro.html', contexto)
    else:
        print("foi por request")
        return render(request, 'usuarios/form_email.html')

def login(request):
    print(">>",request.user.is_authenticated,request.method)
    if not request.user.is_authenticated:
        if request.method == 'POST':
            email = request.POST['email'].lower()
            senha = request.POST['senha']

            user=None
            try:
                user = User.objects.get(email=email.lower()).username
                user = auth.authenticate(request, username=user, password=senha)
                v = user is not None
            except:
                pass
            if user is not None:
                auth.login(request, user)
                print('login realizado com sucesso')
                return redirect('dashboard')
            else:
                erro_a_exibir = {
                        'erro' : 'Usuário/Senha não conferem!'
                    }
                print('\nAlgo errado não estava certo!\n',user,email,senha)
                
                return render(request,'usuarios/login.html',erro_a_exibir)
        return render(request,'usuarios/login.html')
    else:
        return render(request,'usuarios/dashboard.html')

def logout(request):
    auth.logout(request)
    print('Logout realizado com sucesso')
    return redirect('index')

def dashboard(request):
    if request.user.is_authenticated:
        id = request.user.id
        perguntas = Pergunta.objects.order_by('-date_pergunta').filter(user=id)
        dados_assinante = perfil_assinante(request)

        dados = {
            'perguntas' : perguntas,
            'dados_assinante' : dados_assinante
        }
        return render(request, 'usuarios/dashboard.html', dados)
    else:
        print("Usuário não logado")
        return render(request, 'usuarios/login.html')

def meus_dados(request):
    email_user = request.user.email
    #Verifica se o usuário é assinante
    if Assinante.objects.filter(email=email_user).exists():
        dados_assinante = get_object_or_404(Assinante, email=email_user)
    else:
        dados_assinante = None

    dados_geral  = get_object_or_404(User, email=email_user)

    dados = {
        'dados_assinante' : dados_assinante,
        'dados_geral' : dados_geral,
    }
    print(dados_assinante)
    return render(request, 'usuarios/meus_dados.html', dados)

def meu_perfil(request):
    email_user = request.user.email
    data_registro = request.user.date_joined
    
    if User.objects.filter(email=email_user).exists():
        dados_usuario = get_object_or_404(User, email=email_user)
        perguntas = Pergunta.objects.filter(user=request.user)
        ids = set(pergunta.id for pergunta in perguntas)
        lista = list(ids)
        qtd_perguntas = len(lista)
    
    #Verifica se o usuário é assinante
    assinante = perfil_assinante(request)
    # if assinante:
    #     respostas = Pergunta.objects.filter(email_comentario=email_user)
    #     ids = set(resposta.id for resposta in respostas)
    #     lista = list(ids)
    #     qtd_respostas = len(lista)

    # else:
    #    qtd_respostas = None,
    
    score_geral, qtd_likes , qtd_perguntas, qtd_respostas = score(dados_usuario.username,dados_usuario.id)
    dados = {
        'dados_usuario' : dados_usuario,
        'dados_assinante' : assinante,
        'data_registro' : data_registro,
        'qtd_perguntas': qtd_perguntas,
        'qtd_respostas':qtd_respostas,
        'score_geral' : score_geral,
        'qtd_likes' : qtd_likes,
    }
    print(">>>",dados)
    return render(request, 'usuarios/meu_perfil.html', dados)

def meus_comentarios(request):
    email_user = request.user.email
    perguntas = Pergunta.objects.order_by('-date_pergunta').filter(email_comentario=email_user)
    assinante = perfil_assinante(request)

    dados = {
        'perguntas' : perguntas ,
        'dados_assinante' : assinante,
    }
    return render(request, 'usuarios/meus_comentarios.html', dados)

def minhas_perguntas(request):
    id = request.user.id
    assinante = perfil_assinante(request)
    perguntas = Pergunta.objects.order_by('-date_pergunta').filter(user=id)

    dados = {
        'perguntas' : perguntas,
        'dados_assinante' : assinante,
    }
    return render(request, 'usuarios/minhas_perguntas.html', dados)

def form_pergunta(request):
    from perguntas.met_pergunta import remove_emojis
    if request.method == 'POST':
        user = get_object_or_404(User, pk=request.user.id)
        pergunta = request.POST['pergunta']
        print(request.POST['pergunta'])
        faculdade = request.POST['faculdade']
        disciplina = request.POST['disciplina']
        pergunta = remove_emojis(pergunta)
        intro_pergunta = pergunta[0:150]
        nick_pergunta = nick(user)
        print(intro_pergunta)
        pergunta_feita = Pergunta.objects.create(user=user, email_pergunta=user.email,nick_pergunta = nick_pergunta , pergunta=pergunta, intro_pergunta = intro_pergunta , disciplina=disciplina, faculdade=faculdade)
        pergunta_feita.save()
        if Assinante.objects.filter(email=request.user.email).exists():
            score(request.user.email,request.user.id)
        print('Pergunta salva com sucesso')
        return redirect('dashboard')
    else:
        print('algo deu ruim')
        return render(request, 'usuarios/form_pergunta.html')

def cadastro_email(request):
    import string
    alfa_minu = list(string.ascii_lowercase)
    alfa_maiusc = list(string.ascii_uppercase)
    print(alfa_minu,alfa_maiusc, 'a' in alfa_minu, 'G' in alfa_maiusc, 'x' in alfa_maiusc)
    return render(request,'usuarios/form_email.html')

def form_email(request):
    from random import randint
    from datetime import datetime
    from django.core.mail import send_mail

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

        return render(request,'usuarios/form_email_code.html',contexto)
    else:
        contexto = {
            'email' : email,
            'erro' : 'E-mail já cadastrado'
                }

        return render(request,'usuarios/form_email.html',contexto)

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
            return render(request,'usuarios/cadastro.html',contexto)
        
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
        return render(request, 'index.html')

def form_comentar(request):
    if request.method == 'POST':
        id_pergunta = request.POST['teste']
        email_user = request.user.email
        print(">>>",email_user)
        comentario = request.POST['comentario']
        print(comentario)
        Pergunta.objects.filter(id=id_pergunta).update(comentario=comentario, email_comentario=email_user)
        score(email_user,request.user.id)
        print('Pergunta salva com sucesso!!!')
        return redirect('dashboard')
    else:
        print('algo deu ruim')
        return render(request, 'usuarios/form_pergunta.html')

def form_dados(request):
    from django.shortcuts import get_object_or_404
    from django.http import HttpResponse
    import os   
    from pathlib import Path

    if request.method == 'POST':
        user = get_object_or_404(User, pk=request.user.id)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        # Somente altera os dados de assinante se for/foi assinante
        if Assinante.objects.filter(email=request.user.email).exists():
            whatsapp_ddd = request.POST['whatsapp_ddd']
            whatsapp = request.POST['whatsapp']
            instagram = request.POST['instagram']
            linkedIn = request.POST['linkedIn']
            facebook = request.POST['facebook']
            descricao = request.POST['descricao'][:999]


            print("<<>>",request.FILES.getlist('foto',None) == '[ ]', len(request.FILES.getlist('foto',None))==0, whatsapp_ddd)
            # obtém dados do arquivo de foto
            if request.FILES.getlist('foto',None):
                from PIL import Image
                nova_foto = request.FILES.getlist('foto',None)
                file = nova_foto[0].file
                
                
                #Abrindo o arquivo na memória
                from django.conf import settings
                media = 'media/usuarios/'
                name_file = request.POST['cpf'].replace(".","").replace("-","")+'.png'
                path_media = os.path.join(settings.BASE_DIR , '')+media
                path_file = path_media+name_file

                f = open(path_file,'wb')
                f.write(file.getvalue())
                f.close()
                img = Image.open(path_file)
                w,h = img.size
                if w>h:
                    delta = (w-h)/2
                    img = img.crop((delta,0,w-delta,h))
                else:
                    x=14 #retirar uma borda que o processo anterior cria
                    delta = (h-w)/2
                    img = img.crop((x,delta+x,w-x,h-delta-x))

                img = img.resize((120,120),Image.ANTIALIAS)
                img.save(path_file)
                img.close()

                print("Trocou")
                Assinante.objects.filter(assinante=user).update(nome=first_name,sobrenome=last_name,whatsapp=whatsapp,whatsapp_ddd=whatsapp_ddd,instagram=instagram,linkedIn=linkedIn,facebook=facebook,descricao=descricao, foto=media+name_file)
            else:
                print("Não troca")
                Assinante.objects.filter(assinante=user).update(nome=first_name,sobrenome=last_name,whatsapp=whatsapp,whatsapp_ddd=whatsapp_ddd,instagram=instagram,linkedIn=linkedIn,facebook=facebook,descricao=descricao)
        

            # Salva todas as novas informações (Email e CPF são imutáveis) 
            
        User.objects.filter(email=request.user.email).update(first_name=first_name,last_name=last_name,username=request.user.email)
        
        print('Dados salvos com sucesso')
        return redirect('../meus_dados')
    else:
        #
        return render(request, 'index.html')

def revisar(request):
    dados_assinante = perfil_assinante(request)
    id = request.POST['id_pergunta']
    pergunta = get_object_or_404(Pergunta,id=id)
    # Pergunta.objects.filter(id=id).update(revisao_solicitada=True,revisao_qtd=pergunta.revisao_qtd+1)

    # #verifica se há revisão anterior (Cria ou insere mais um comentário)
    # if not Revisao.objects.filter(id_pergunta=id).exists():
    #     revisao_feita = Revisao.objects.create(id_pergunta=pergunta,email_revisor=request.user.email,comentario_revisao ="Essa é a revisão")
    #     revisao_feita.save()
    # else:
    #     Revisao.objects.filter(id=id).update(email_revisor=request.user.email,comentario_revisao ="Essa é a revisão da revisaõ 2")
    print("REVISAR", dados_assinante)
    contexto = {
        'dados_assinante' : dados_assinante,
        'pergunta' : pergunta
    }
    return render(request, 'usuarios/revisao.html',contexto)
    
def form_revisar(request):
    dados_assinante = perfil_assinante(request)
    id = request.POST['id_pergunta']
    comentario_revisao = request.POST['revisao_efetuada']
    pergunta = get_object_or_404(Pergunta,id=id)
    Pergunta.objects.filter(id=id).update(revisao_solicitada=True,revisao_qtd=pergunta.revisao_qtd+1)
    #verifica se há revisão anterior (Cria ou insere mais um comentário)
    print("xxx",Revisao.objects.filter(email_revisor=request.user.email,id_pergunta=id).exists())
    if not Revisao.objects.filter(email_revisor=request.user.email,id_pergunta=id).exists():
        revisao_feita = Revisao.objects.create(id_pergunta=pergunta,email_revisor=request.user.email,comentario_revisao=comentario_revisao)
        revisao_feita.save()
    else:
        Revisao.objects.filter(email_revisor=request.user.email,id_pergunta=id).update(email_revisor=request.user.email,comentario_revisao=comentario_revisao)
    
    contexto = {
        'dados_assinante' : dados_assinante
    }
    return render(request, 'usuarios/revisao_envio.html',contexto)
    
def ver_minha_colaboracao(request, pergunta_id):

    pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
    #Obtém o email de que eventualmente ja respondeu a pergunta
    email_user_pergunta = pergunta.email_comentario

    try:
        #Dados do usuário logado
        email_usuario = request.user.email
    except:
        #Caso esteja anônimo
        email_usuario = None

    try:
        assinante=None
        usuario_logado=None
        #Verifica se quem respondeu está assinante
        if email_user_pergunta:
            assinante =  Assinante.objects.filter(email=email_user_pergunta, mensalidade=True)
            if assinante:
                #se o quem respondeu estiver assinante
                assinante =  get_object_or_404(Assinante, email=email_user_pergunta)
            else:
                assinante = None

        #Verifica se o usuário logado está assinante
        if email_usuario:
            usuario_logado =  Assinante.objects.filter(email=email_usuario, mensalidade=True)
            if usuario_logado:
                #se estiver assinante
                usuario_logado =  get_object_or_404(Assinante, email=email_usuario)
            else:
                usuario_logado = None

        contexto = {
        'dados_assinante': assinante,
        'usuario_logado':usuario_logado,
        'pergunta' : pergunta,
        'usuario_assinante_comentario':assinante ,
        }
        
        return render(request,'pergunta.html', contexto )
    
    except AttributeError:

        contexto = {
            'pergunta' : pergunta,
            'assinante' : None ,
            'usuario_logado':None,
        }
        return render(request,'pergunta.html', contexto )

def perfil_assinante(request):
    email_user = request.user.email
    if Assinante.objects.filter(email=email_user).exists():
        assinante = get_object_or_404(Assinante,email=email_user)
    else:
        assinante = None
    print("Assinante:",assinante)
    return assinante

def curtir(request):
    import json
    from django.http import HttpResponse

    if request.user.is_active: 
        pass

        if request.method == "POST":
            id = request.POST.get('content_id')
            pergunta = get_object_or_404(Pergunta,id=id)
            # dados do usuário assinante -> para calcular a pontuação
            user_score = pergunta.user
            user_score_id = get_object_or_404(User,email=user_score).id
            
            # insere like no BD ou apaga se retirar a curtida
            if LikeBtn.objects.filter(user=request.user,id_pergunta = id).exists():
                like_user = get_object_or_404(LikeBtn,user=request.user,id_pergunta=id)
                LikeBtn.objects.filter(pk=like_user.pk).delete()
                like_status=False
            else:
                
                like_status = True
                LikeBtn.objects.create(user=request.user,id_pergunta=pergunta,likes=like_status)
                
        #cálculo da pontuação
        score(user_score,user_score_id)
        contexto={"liked":like_status,"content_id":id}

        return HttpResponse(json.dumps(contexto), content_type='application/json')
    
    else:
        print("Usuário não logado")
        contexto={"liked":None,"content_id":None}
        return HttpResponse({json.dumps(contexto)}, content_type='application/json')

def perfil(request, perfil_id):
    perfil = get_object_or_404(Assinante,id=perfil_id)
    perfil_geral =get_object_or_404(User,email=perfil.email)
    print(perfil,perfil_geral)
    score_geral, qtd_likes , qtd_perguntas, qtd_respostas = score(perfil_geral.username,perfil_geral.id)

    contexto ={
        'dados_usuario': perfil_geral,
        'dados_assinante':perfil,
        'data_registro' : perfil_geral.date_joined,
        'qtd_perguntas': qtd_perguntas,
        'qtd_respostas': qtd_respostas,
        'score_geral' : score_geral,
        'qtd_likes' : qtd_likes,
    }
    return render(request,"usuarios/perfil.html",contexto)

def planos(request):

    contexto = {

    }
    return render(request,'usuarios/planos.html',contexto)

def assessores(request):    
    assinantes = Assinante.objects.filter(mensalidade=True).order_by('?')
    print(assinantes)
    descricoes = set(assinante.descricao[0:20] for assinante in assinantes)
    print(descricoes)
    contexto = {
        'assinantes':assinantes,
    }
    print(">>>",assinantes)
    return render(request,'usuarios/assessores.html',contexto)
