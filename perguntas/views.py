import email
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import Pergunta, LikeBtn
# from usuarios.models import Assinante
# from usuarios.views import perfil_assinante
Assinante = None

def index(request):
    perguntas = Pergunta.objects.order_by('-date_pergunta').filter(publicada=True)
    dados = {
        'perguntas' : perguntas
    }
    return render(request,'index.html', dados)


def pergunta(request, pergunta_id):
    from perguntas.met_pergunta import colaborador_aleatorio, usuario_assinante_comentario , usuario_logado_assinante
    # Dados da pergunta
    pergunta = get_object_or_404(Pergunta, pk=pergunta_id) 
    likes_count = LikeBtn.objects.filter(id_pergunta = pergunta.pk).count() # Qtd de Likes
    email_usuario_comentario = pergunta.email_comentario  #Obtém o email de que eventualmente ja respondeu a pergunta
    
    user_anonimo = None
    if pergunta.comentario != '':
        usuario_comentario = get_object_or_404(Assinante,email=email_usuario_comentario)
        user_comentario =  usuario_assinante_comentario(email_usuario_comentario)
        user_anonimo = email_usuario_comentario[:email_usuario_comentario.find('@')]+usuario_comentario.whatsapp[-4:]
    else:
        user_comentario = None

    # Verifica se quem está acessando está logado ou é anônimo
    if request.user.is_active: 
        email_usuario = request.user.email

        # Verifica se o usuário logado deu Like na pergunta.
        my_like = False
        if LikeBtn.objects.filter(user = request.user , id_pergunta = pergunta.pk).exists():
            my_like = True
            likes_count -= 1

        #gera o usuário para as perguntas
        d = str(pergunta.user.date_joined)
        id_user = d[d.find(' ')-1:d.find(':')].replace(':','').replace(' ','')
        user_pergunta = pergunta.user

        contexto = {
        'usuario_assinante_comentario' : user_comentario ,
        'usuario_logado_assinante': usuario_logado_assinante(email_usuario),
        'assinante_random':colaborador_aleatorio(pergunta),
        'pergunta' : pergunta,
        'my_like' : my_like,
        'likes_count':likes_count,
        'usuario_anonimo': user_anonimo ,
        'usuario_pergunta':str(user_pergunta)[:str(user_pergunta).find('@')]+id_user,
        }

        return render(request,'pergunta.html', contexto )
    
    else:
        contexto = {
        'usuario_assinante_comentario' : usuario_assinante_comentario(email_usuario_comentario),
        'usuario_logado_assinante':None,
        'assinante_random':colaborador_aleatorio(pergunta),
        'pergunta' : pergunta,
        'my_like' : False,
        'likes_count':likes_count,
        }
        return render(request,'pergunta.html', contexto )


def ultimas_perguntas(request):
    perguntas = Pergunta.objects.order_by('-date_pergunta').filter(publicada=True)[0:100]
    print(perguntas)
    # perguntas.append('teste':'Working')
    print(perguntas)
    #gera o usuário para as perguntas
    # d = str(pergunta.user.date_joined)
    # id_user = d[d.find(' ')-1:d.find(':')].replace(':','').replace(' ','')
    # user_pergunta = pergunta.user

    contexto = {
        'perguntas' : perguntas,            
        'faculdade_select':None,
        'disciplina_select':None,
        # 'usuario_pergunta':str(user_pergunta)[:str(user_pergunta).find('@')]+id_user,
        }
    print(">>>",pergunta,contexto)
    return render(request,'ultimas_perguntas.html', contexto )


def filtro_ultimas_perguntas(request):
    if request.method == 'POST':   
        faculdade = request.POST['faculdade']
        disciplina = request.POST['disciplina']
        status = request.POST['status']
        
        if status == 'TODAS':
            perguntas = Pergunta.objects.order_by('-date_pergunta').filter(faculdade__contains=faculdade,disciplina__contains=disciplina,publicada=True)[0:100]
        elif status == 'AGUARDANDO COMENTÁRIOS':
            perguntas = Pergunta.objects.order_by('-date_pergunta').filter(faculdade__contains=faculdade,disciplina__contains=disciplina, comentario__exact = '' ,publicada=True)[0:100]
        elif status == 'RESPONDIDAS':
            perguntas = Pergunta.objects.order_by('-date_pergunta').filter(faculdade__contains=faculdade,disciplina__contains=disciplina, publicada=True).exclude(comentario__exact ='')[0:100]
        
        print(">>>AAS",faculdade,disciplina)
        contexto = {
            'perguntas' : perguntas,
            'faculdade_select':faculdade,
            'disciplina_select':disciplina,
            'status_select':status,
        }
        print("WWW",contexto)
        return render(request,'ultimas_perguntas.html', contexto )

    else:
        perguntas = Pergunta.objects.order_by('-date_pergunta').filter(faculdade='UNICESUMAR',disciplina='GESTÃO',publicada=True)[0:100]
    contexto = {
        'perguntas' : perguntas,            
        'faculdade_select':None,
        'disciplina_select':None,
        }
    print(">>>bbb",pergunta,contexto)
    return render(request,'ultimas_perguntas.html', contexto )


def buscar(request):
    lista_perguntas = Pergunta.objects.order_by('-date_pergunta').filter(publicada=True)

    if 'buscar' in request.GET:
        nome_a_buscar = request.GET['buscar']
        if buscar:
            lista_perguntas = lista_perguntas.filter(pergunta__icontains=nome_a_buscar)

    dados = {
        'perguntas' : lista_perguntas,
        'busca' : nome_a_buscar
    }

    return render(request, 'buscar.html', dados)


def ver_minha_colaboracao(request,pergunta_id):
    pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
    contexto = {
         'pergunta' : pergunta,
        }
    return render(request,'ver_minha_colaboracao.html', contexto )


def assinante_ran(pergunta):
    import random
    #Obtém todos os assinante atuais
    assinantes = Assinante.objects.filter( mensalidade=True)
    #cria uma lista de todos os assintantes
    email = []
    for i in range(len(list(assinantes))):
        email.append(assinantes[i].email)
    print("list_email",email)
    #Faz uma escolha aleatória dentro da lista
    print("email ass",pergunta.email_comentario)
    while(pergunta.email_comentario):
        email_random = random.choice(email)
        if email_random != pergunta.email_comentario:
            email = email_random
            print("WWW",pergunta.email_comentario==email,email)
            break
    assinante = Assinante.objects.get(email=email)
    print("<><><>",assinante)
    return assinante
