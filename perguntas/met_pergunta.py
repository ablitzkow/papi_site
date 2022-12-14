from usuarios.models import Assinante, Especialidade
from django.shortcuts import get_object_or_404

#Obtém um colaborador aleatório

def colaborador_aleatorio_orig(pergunta , comentario):
    from django.db.models import Q
    import random
    

    if Especialidade.objects.filter(disciplina = pergunta.disciplina, faculdade = pergunta.faculdade , exclusivo = True).exists():
        especialista = get_object_or_404(Especialidade,disciplina = pergunta.disciplina)
        assinante_selecionado = especialista.assinante
        assinante_random = get_object_or_404(Assinante,email=assinante_selecionado.assinante)

    elif Especialidade.objects.filter(disciplina = pergunta.disciplina, faculdade = pergunta.faculdade , exclusivo = False).exists():
        
        #se existir apenas um cadastro 
        if Especialidade.objects.filter(disciplina = pergunta.disciplina).count()==1:
            especialista = get_object_or_404(Especialidade,disciplina = pergunta.disciplina)
            assinante_selecionado = especialista.assinante

            #Verifica a vez de quem é a de aparecer:
            if especialista.rodada == True:
                Especialidade.objects.filter(assinante = especialista.assinante).update(rodada = False)
                email=especialista.assinante
            else:
                Especialidade.objects.filter(assinante = especialista.assinante).update(rodada = True)
                import random
                # opçoes = ['blitzkow@gmail.com','mota.christopher@gmail.com']
                opçoes = ['blitzkow@gmail.com']
                email = random.choice(opçoes)
                
            # Obtém os dados da Assinatura
            assinante_random = get_object_or_404(Assinante,email=email)

        # Será executado se houver mais de 1 assessor cadastrado, modo aleatório
        else:
            assinante_selecionado = Especialidade.objects.filter(Q(disciplina = pergunta.disciplina) | Q(disciplina='TODAS')).order_by('?').first()
            assinante_random = Assinante.objects.filter(email=assinante_selecionado.assinante)
            assinante_random = get_object_or_404(Assinante,email=assinante_selecionado.assinante)
    
    # Será executado se não houver nenhum assessor cadastrado
    else:
        opçoes = ['blitzkow@gmail.com','mota.christopher@gmail.com']
        #opçoes = ['mota.christopher@gmail.com']
        email = random.choice(opçoes)
        assinante_random = get_object_or_404(Assinante,email=email)

        #assinante_random = get_object_or_404(Assinante,email='blitzkow@gmail.com')
    
    print("Assessor selecionado:",assinante_random)
    return assinante_random


def colaborador_aleatorio(pergunta , comentario):
    from django.db.models import Q
    import random
    
    # se houver algum exclusivo, se e somente um:
    if Especialidade.objects.filter(faculdade = pergunta.faculdade , disciplina = pergunta.disciplina,  exclusivo = True).exists() and Especialidade.objects.filter(faculdade = pergunta.faculdade , disciplina = pergunta.disciplina,  exclusivo = True).count()==1:
        especialista = get_object_or_404(Especialidade, faculdade = pergunta.faculdade , disciplina = pergunta.disciplina, exclusivo = True)
        assinante_selecionado = especialista.assinante
        assinante_random = get_object_or_404(Assinante,email=assinante_selecionado.assinante)

    elif Especialidade.objects.filter(disciplina = pergunta.disciplina, faculdade = pergunta.faculdade , exclusivo = False).exists():
        print("OK1.0")
        if Especialidade.objects.filter(disciplina = pergunta.disciplina).count()==1:
            print("OK2.1")
            especialista = get_object_or_404(Especialidade,disciplina = pergunta.disciplina)
            assinante_selecionado = especialista.assinante
            
            # verifica o modelo de peso
            if especialista.peso == 0:
                print("OK3.1")
                # Se igual a 0 é porque está em 50%
                # Verifica a vez de quem é a de aparecer:
                if especialista.rodada == True:
                    print("OK4.1")
                    Especialidade.objects.filter(assinante = especialista.assinante).update(rodada = False)
                    email=especialista.assinante
                else:
                    print("OK4.2")
                    Especialidade.objects.filter(assinante = especialista.assinante).update(rodada = True)
                    import random
                    # opçoes = ['blitzkow@gmail.com','mota.christopher@gmail.com']
                    opçoes = ['blitzkow@gmail.com']
                    email = random.choice(opçoes)
                
                # Obtém os dados da Assinatura
                assinante_random = get_object_or_404(Assinante,email=email)
                    
            else:
                print("OK3.2")
                # Foi inserido um peso para a divulgação
                pesos = [1,2,3,4,5,6,7,8,9,10]
                peso = random.choice(pesos)
                print("peso:",peso)

                if peso<=especialista.peso:
                    email = especialista.assinante
                else:
                    # opçoes = ['blitzkow@gmail.com','mota.christopher@gmail.com']
                    # email = random.choice(opçoes)
                    email = 'blitzkow@gmail.com'
                
                # Obtém os dados da Assinatura
                assinante_random = get_object_or_404(Assinante,email=email)
                    
        # Será executado se houver mais de 1 assessor cadastrado, modo aleatório ou outro erro desconhecido.
        else:
            print("OK2.2")
            assinante_selecionado = Especialidade.objects.filter(Q(disciplina = pergunta.disciplina) | Q(disciplina='TODAS')).order_by('?').first()
            assinante_random = Assinante.objects.filter(email=assinante_selecionado.assinante)
            assinante_random = get_object_or_404(Assinante,email=assinante_selecionado.assinante)
    
    # Será executado se não houver nenhum assessor cadastrado
    else:
        print("OK1.1")
        #opçoes = ['blitzkow@gmail.com','mota.christopher@gmail.com']
        #opçoes = ['mota.christopher@gmail.com']
        opçoes = ['blitzkow@gmail.com']
        email = random.choice(opçoes)
        assinante_random = get_object_or_404(Assinante,email=email)
    
    print("RAND",assinante_random)
    return assinante_random




def usuario_assinante_comentario(email_usuario_comentario):
    from django.shortcuts import render, get_object_or_404
    if Assinante.objects.filter(email=email_usuario_comentario, mensalidade=True).exists():
            #se o quem respondeu estiver assinante
            return  get_object_or_404(Assinante, email=email_usuario_comentario)
    # Retorna None caso quem respondeu não esteja assinante
    return None

def usuario_logado_assinante(email_usuario):
        from django.shortcuts import render, get_object_or_404

        #Verifica se o usuário logado está assinante
        if  Assinante.objects.filter(email=email_usuario, mensalidade=True).exists():
            return  get_object_or_404(Assinante, email=email_usuario)
        else:
            return None


def remove_emojis(data):
    import re
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)

def nick_user(user):
    d = str(user.date_joined)
    id_user = d[d.find(' ')-1:d.find(':')].replace(':','').replace(' ','')
    nick = str(user)[:str(user).find('@')]+id_user
    return nick