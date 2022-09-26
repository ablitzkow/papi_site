from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from perguntas.models import Comentario, Pergunta, Revisao , LikeBtn
from usuarios.models import Assinante , Registro_Email
from usuarios.score import score


def dados_cadastro(request):
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
            return render(request,'usuarios/form/dados_cadastro.html', erro_a_exibir)
        
        #verifica se as senhas são iguais
        elif password != password2:
            contexto = {
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'erro' : 'Senhas não coincidem'
            }
            print("Senhas não coincidem")
            return render(request,'usuarios/form/dados_cadastro.html', contexto)
            
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
                return render(request,'usuarios/form/dados_cadastro.html', contexto)
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
                return render(request,'usuarios/form/dados_cadastro.html', contexto)
    else:
        return redirect('cadastro')

def login(request):
    print(">>",request.user.is_authenticated,request.method, request.GET['action'])
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
                if request.GET['action']=="logar":
                    return redirect('dashboard')
                else:
                    return redirect('form_pergunta')
            else:
                erro_a_exibir = {
                        'erro' : 'Usuário/Senha não conferem!'
                    }
                print('\nAlgo errado não estava certo!\n',user,email,senha)
                
                return render(request,'usuarios/login.html',erro_a_exibir)
        return render(request,'usuarios/login.html',{'action':request.GET['action']})
    else:
        return render(request,'usuarios/dashboard.html')

def logout(request):
    auth.logout(request)
    print('Logout realizado com sucesso')
    return redirect('index')

def dashboard(request):
    if request.user.is_authenticated:
        id = request.user.id
        perguntas = Pergunta.objects.order_by('-data').filter(user=id)
        assinante = perfil_assinante(request)

        dados = {
            'perguntas' : perguntas,
            'assinante' : assinante
        }
        return render(request, 'usuarios/dashboard.html', dados)
    else:
        print("Usuário não logado")
        return render(request, 'usuarios/login.html')

def meus_dados(request):
    email_user = request.user.email
    #Verifica se o usuário é assinante
    if Assinante.objects.filter(email=email_user).exists():
        assinante = get_object_or_404(Assinante, email=email_user)
    else:
        assinante = None

    dados_geral  = get_object_or_404(User, email=email_user)

    dados = {
        'assinante' : assinante,
        'dados_geral' : dados_geral,
    }
    print(assinante)
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
    
    # Dados do assinante
    assinante = perfil_assinante(request)
    
    score_geral, qtd_likes , qtd_perguntas, qtd_respostas = score(dados_usuario.username,dados_usuario.id)
    dados = {
        'dados_usuario' : dados_usuario,
        'assinante' : assinante,
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
    comentarios = Comentario.objects.order_by('-data').filter(email=email_user)
    ids = set(comentario.id_pergunta_id for comentario in comentarios)
    print("\n\n\n\n>>>>a",ids)
    perguntas = Pergunta.objects.order_by('-data').filter(id__in = ids)
    print(perguntas)
    assinante = perfil_assinante(request)

    dados = {
        'perguntas' : perguntas ,
        'assinante' : assinante,
    }
    return render(request, 'usuarios/meus_comentarios.html', dados)

def minhas_perguntas(request):
    id = request.user.id
    assinante = perfil_assinante(request)
    perguntas = Pergunta.objects.order_by('-data').filter(user=id)

    dados = {
        'perguntas' : perguntas,
        'assinante' : assinante,
    }
    return render(request, 'usuarios/minhas_perguntas.html', dados)

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
                Assinante.objects.filter(assinante=user).update(nome=first_name,sobrenome=last_name,whatsapp=whatsapp,whatsapp_ddd=whatsapp_ddd,instagram=instagram,linkedIn=linkedIn,facebook=facebook,descricao=descricao, foto=media+name_file)
            else:
                Assinante.objects.filter(assinante=user).update(nome=first_name,sobrenome=last_name,whatsapp=whatsapp,whatsapp_ddd=whatsapp_ddd,instagram=instagram,linkedIn=linkedIn,facebook=facebook,descricao=descricao)
        

        # Salva todas as novas informações (Email e CPF são imutáveis) 
        User.objects.filter(email=request.user.email).update(first_name=first_name,last_name=last_name,username=request.user.email)
        
        print('Dados salvos com sucesso')
        return redirect('../meus_dados')
    else:
        return render(request, 'index.html')

def revisar(request):
    assinante = perfil_assinante(request)
    id = request.POST['id_url']
    pergunta = get_object_or_404(Pergunta,id_url=id)
    contexto = {
        'assinante' : assinante,
        'pergunta' : pergunta
    }
    return render(request, 'usuarios/revisao.html',contexto)
    
def form_revisar(request):
    assinante = perfil_assinante(request)
    
    id = request.POST['id_url']
    print("Aqui",id)
    print("Aqui00")
    revisao = request.POST['revisao_efetuada']
    pergunta = get_object_or_404(Pergunta,id_url=id)
    print("Aqui")
    comentario = get_object_or_404(Comentario,id_pergunta = id)
    #Verifica se já houve pedido de revisão

    rev = Revisao.objects.create(id_pergunta=pergunta,email=request.user.email,revisao=revisao)
    rev.save()
    Comentario.objects.update(id_pergunta=id,revisao_solicitada=True , revisao_qtd=comentario.revisao_qtd+1)

    #verifica se há revisão anterior (Cria ou insere mais um comentário)
    # print("xxx",Revisao.objects.filter(email=request.user.email,id_pergunta=id).exists())
    # if not Revisao.objects.filter(email=request.user.email,id_pergunta=id).exists():
    #     revisao_feita = Revisao.objects.create(id_pergunta=pergunta,email=request.user.email,revisao=revisao)
    #     revisao_feita.save()
    # else:
    #     Revisao.objects.filter(email=request.user.email,id_pergunta=id).update(email=request.user.email,revisao=revisao)
    
    contexto = {
        'assinante' : assinante
    }
    return render(request, 'usuarios/revisao_envio.html',contexto)
    
def ver_minha_colaboracao(request, pergunta_id):

    comentario = get_object_or_404(Comentario, pk=pergunta_id)
    #Obtém o email de que eventualmente ja respondeu a pergunta
    email_user_pergunta = comentario.email

    try:
        #Dados do usuário logado
        email_usuario = request.user.email
    except:
        #Caso esteja anônimo
        email_usuario = None

    try:
        assinante=None
        usuario_logado=None
        #####
        ##### VERIFICAR O TRECHO ABAIXO, SUBSTITUIR PELO MÉTODO ASSINANTE(REQUEST)
        #####
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
        'assinante': assinante,
        'usuario_logado':usuario_logado,
        'pergunta' : comentario,
        'usuario_assinante_comentario':assinante ,
        }
        
        return render(request,'perguntas/pergunta.html', contexto )
    
    except AttributeError:

        contexto = {
            'pergunta' : comentario,
            'assinante' : None ,
            'usuario_logado':None,
        }
        return render(request,'perguntas/pergunta.html', contexto )

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
            comentario = get_object_or_404(Comentario,id_pergunta=id)
            # dados do usuário assinante -> para calcular a pontuação
            user_score = comentario.email
            user_score_id = get_object_or_404(User,email=user_score).id
            
            # insere like no BD ou apaga se retirar a curtida
            if LikeBtn.objects.filter(user=request.user,id_pergunta = id).exists():
                like_user = get_object_or_404(LikeBtn,user=request.user,id_pergunta=id)
                LikeBtn.objects.filter(pk=like_user.pk).delete()
                like_status=False
            else:
                like_status = True
                LikeBtn.objects.create(user=request.user,id_pergunta=get_object_or_404(Pergunta,id=id),likes=like_status)
                
        #cálculo da pontuação
        print(user_score,user_score_id)
        score(user_score,user_score_id)
        contexto={"liked":like_status,"content_id":id}

        return HttpResponse(json.dumps(contexto), content_type='application/json')
    
    else:
        print("Usuário não logado")
        contexto={"liked":None,"content_id":None}
        return HttpResponse({json.dumps(contexto)}, content_type='application/json')

def perfil(request, id_perfil):
    perfil = get_object_or_404(Assinante,id_perfil = id_perfil)
    perfil_geral =get_object_or_404(User,email=perfil.email)
    score_geral, qtd_likes , qtd_perguntas, qtd_respostas = score(perfil_geral.username,perfil_geral.id)

    contexto ={
        'dados_usuario': perfil_geral,
        'assinante':perfil,
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

