import email
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import Comentario, Pergunta, LikeBtn
from usuarios.models import Assinante
from usuarios.views import perfil_assinante


def pergunta(request, id_url):
    from perguntas.met_pergunta import colaborador_aleatorio,usuario_assinante_comentario,usuario_logado_assinante, nick_user
    # Dados da pergunta
    if Pergunta.objects.filter(id_url=id_url).exists():
        #Obtém a pergunta pelo ID
        pergunta = get_object_or_404(Pergunta, id_url=id_url)
        if pergunta.publicada == True or pergunta.email == request.user.email:
            likes_count = LikeBtn.objects.filter(id_pergunta = pergunta.pk).count() # Qtd de Likes
            # Formata pelo tamanho da pergunta
            if len(pergunta.pergunta)>=1750:
                n = pergunta.pergunta[700:].find("\n")
                pergunta_inicio = pergunta.pergunta[:700+n].replace('\n','<br>')
                pergunta_fim = pergunta.pergunta[700+n+1:].replace('\n','<br>')
            else:
                pergunta_inicio = None
                pergunta_fim = None
            #Obtém dados de quem respondeu a pergunta
            if Comentario.objects.filter(id_pergunta=pergunta.id).exists():
                comentario = get_object_or_404(Comentario,id_pergunta_id=pergunta.id)
                assinante = get_object_or_404(Assinante, email = comentario.email)
                email_comentario = usuario_assinante_comentario(comentario.email)
                comentario_texto = comentario.comentario.replace('\n','<br>')  
                if not assinante.mensalidade:
                    assinante = None
            else:
                comentario = None
                assinante = None
                email_comentario = None
                comentario_texto = ""
            
            # Seleciona um colaborador aleatório
            assinante_aleatorio = colaborador_aleatorio(comentario)
            assinante_random_descricao = assinante_aleatorio.descricao.replace('\n','<br>')
            
            # Verifica se quem está acessando está logado ou é anônimo
            if request.user.is_active: 
                email_usuario = request.user.email
                # Verifica se o usuário logado deu Like na pergunta.
                my_like = False
                if LikeBtn.objects.filter(user = request.user , id_pergunta = pergunta.id).exists():
                    my_like = True
                    likes_count -= 1
                pergunta_texto = pergunta.pergunta.replace('\n','<br>')

                # Verifica se tem comentário, para enviar form Recaptcha
                if not pergunta.comentario_check:
                    from usuarios.forms import ReCaptcha
                    recaptcha = ReCaptcha()
                else:
                    recaptcha = None
                
                contexto = {
                'title' : 'Papiron - '+pergunta.faculdade+' - '+pergunta.intro_pergunta,
                'pergunta'  : pergunta,
                'comentario': comentario,
                'pergunta_texto':pergunta_texto,
                'pergunta_inicio':pergunta_inicio,
                'pergunta_fim':pergunta_fim,
                'comentario_texto':comentario_texto,
                'usuario_assinante_comentario' : email_comentario,
                'assinante':assinante,
                'assinante_random':assinante_aleatorio,
                'usuario_logado_assinante': usuario_logado_assinante(email_usuario),
                'assinante_random_descricao':assinante_random_descricao,
                'my_like' : my_like,
                'likes_count':likes_count,
                'recaptcha' : recaptcha ,
                }
                return render(request,'perguntas/pergunta.html', contexto )
            
            else:
                pergunta_texto = pergunta.pergunta.replace('\n','<br>')

                contexto = {
                'title' : 'Papiron - '+pergunta.faculdade+' - '+pergunta.intro_pergunta,
                'pergunta'  : pergunta,
                'comentario': comentario,
                'pergunta_texto':pergunta_texto,
                'pergunta_inicio':pergunta_inicio,
                'pergunta_fim':pergunta_fim,
                'comentario_texto':comentario_texto,
                'usuario_assinante_comentario' : email_comentario,
                'assinante': assinante,
                'assinante_random':assinante_aleatorio,
                'usuario_logado_assinante': None,
                'assinante_random_descricao':assinante_random_descricao,
                'my_like' : False,
                'likes_count':likes_count,
                'recaptcha' : None ,
                }
                # contexto = {
                # 'usuario_assinante_comentario' : email_comentario ,
                # 'usuario_logado_assinante':None,
                # 'assinante_random':colaborador_aleatorio(comentario),
                # 'pergunta' : pergunta,
                # 'comentario': comentario,
                # 'assinante' :assinante,
                # 'my_like' : False,
                # 'likes_count':likes_count,
                # }
                return render(request,'perguntas/pergunta.html', contexto )
    else:
        return render(request,'index.html')


def ultimas_perguntas(request):
    from datetime import datetime, timedelta
    data = datetime.today()-timedelta(days=30)
    perguntas = Pergunta.objects.order_by('-data').filter(data__gte=data,publicada=True)[0:100]
    contexto = {
        'perguntas' : perguntas,        
        'faculdade_select':None,
        'disciplina_select':None,
        }

    return render(request,'perguntas/ultimas_perguntas.html', contexto)


def analisar_perguntas(request):
    if request.user.is_superuser:
        from datetime import datetime, timedelta
        data = datetime.today()-timedelta(days=7)
        perguntas = Pergunta.objects.order_by('-data').filter(data__gte=data,publicada=False)[0:100]
        contexto = {
            'perguntas' : perguntas,        
            'faculdade_select':None,
            'disciplina_select':None,
            }

        return render(request,'perguntas/analisar_perguntas.html', contexto)
    else:
        return render(request,'500.html')


def filtro_ultimas_perguntas(request):
    if request.method == 'POST':   
        faculdade = request.POST['faculdade']
        disciplina = request.POST['disciplina']
        status = request.POST['status']
        
        if status == 'TODAS':
            perguntas = Pergunta.objects.order_by('-data').filter(faculdade__contains=faculdade,disciplina__contains=disciplina,publicada=True)[0:100]
        elif status == 'AGUARDANDO COMENTÁRIOS':
            perguntas = Pergunta.objects.order_by('-data').filter(faculdade__contains=faculdade,disciplina__contains=disciplina, comentario_check__exact = False ,publicada=True)[0:100]
        elif status == 'RESPONDIDAS':
            perguntas = Pergunta.objects.order_by('-data').filter(faculdade__contains=faculdade,disciplina__contains=disciplina, publicada=True, comentario_check__exact = True)[0:100]
        
        print(">>>AAS",faculdade,disciplina)
        contexto = {
            'perguntas' : perguntas,
            'faculdade_select':faculdade,
            'disciplina_select':disciplina,
            'status_select':status,
        }
        print("WWW",contexto)
        return render(request,'perguntas/ultimas_perguntas.html', contexto )

    else:
        perguntas = Pergunta.objects.order_by('-data').filter(faculdade='UNICESUMAR',disciplina='GESTÃO',publicada=True)[0:100]
    contexto = {
        'perguntas' : perguntas,            
        'faculdade_select':None,
        'disciplina_select':None,
        }
    print(">>>bbb",pergunta,contexto)
    return render(request,'perguntas/ultimas_perguntas.html', contexto )


def buscar(request):
    busca = ''
    if 'buscar' in request.GET:
        busca = request.GET['buscar']
    else:
        busca = request.POST['buscar']

    if Pergunta.objects.order_by('-data').filter(pergunta__icontains=busca,publicada=True).exists():
        lista_perguntas = Pergunta.objects.order_by('-data').filter(publicada=True)
        perguntas = lista_perguntas.filter(pergunta__icontains=busca)
    else:
        perguntas = None

    contexto = {
        'perguntas' : perguntas,           
        'faculdade_select':None,
        'disciplina_select':None,
        'busca' : busca
        }

    return render(request, 'perguntas/resultado_busca.html', contexto)


def ver_minha_colaboracao(request,pergunta_id):
    pergunta = get_object_or_404(Pergunta, pk=pergunta_id)
    contexto = {
         'pergunta' : pergunta,
        }
    return render(request,'usuarios/ver_minha_colaboracao.html', contexto )


def assinante_ran(pergunta):
    import random
    #REFAZERRRR EMAIL COMENTARIO
    #Obtém todos os assinante atuais
    assinantes = Assinante.objects.filter( mensalidade=True)
    #cria uma lista de todos os assintantes
    email = []
    for i in range(len(list(assinantes))):
        email.append(assinantes[i].email)
    print("list_email",email)
    #Faz uma escolha aleatória dentro da lista
    while(pergunta.email_comentario):
        email_random = random.choice(email)
        if email_random != pergunta.email_comentario:
            email = email_random
            print("WWW",pergunta.email_comentario==email,email)
            break
    assinante = Assinante.objects.get(email=email)
    print("<><><>",assinante)
    return assinante


######### def para Robots #######

def auto_publicar(request):
    from django.http import HttpResponse
    from datetime import datetime, timedelta
    data = datetime.today()-timedelta(days=7)
    perguntas= Pergunta.objects.order_by('-data').filter(data__lte=data,publicada=False).update(publicada=True)
    return HttpResponse(status=200, content='Essas são as perguntas'+str(perguntas))