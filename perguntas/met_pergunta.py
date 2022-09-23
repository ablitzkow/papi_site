from usuarios.models import Assinante

#Obtém um colaborador aleatório
def colaborador_aleatorio(comentario):
    assinante_random = Assinante.objects.filter(mensalidade=True).order_by('?').first()
    while comentario:
        print("AAAA", assinante_random,assinante_random.foto)
        if assinante_random:
            if assinante_random.email != comentario.email:
                assinante_random = Assinante.objects.get(email=assinante_random.email)
                break
        else:
            assinante_random = None
            break
        assinante_random = Assinante.objects.filter(mensalidade=True).order_by('?').first()
    print("AAAA", assinante_random,assinante_random.foto)
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