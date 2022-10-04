from django.shortcuts import render, HttpResponse

def index(request):
    
    return render(request,'index.html')

def sitemap(request):
    from . import settings
    return HttpResponse(open(str(settings.BASE_DIR)+'/papiron/sitemap.xml').read(), content_type='text/xml')

def gera_sitemap(request):
    from . import settings
    from perguntas.models import Pergunta
    from .sitemap import xml_url, sitemap_insert,hoje,xml_alterar_data, sitemap_delete
    # pesquisa Perguntas publicadas
    perguntas = Pergunta.objects.filter(publicada=True)
    ids = set(pergunta.id_url for pergunta in perguntas)
    data = hoje()
    # Acessa arquivo sitemap.xml
    file = str(settings.BASE_DIR)+'/papiron/sitemap.xml'
    # leitura dos URL´s listados
    list = xml_url(file)
    for id in ids:
        url = 'https://www.papiron.com.br/perguntas/'+str(id)
        if not url in list:
            sitemap_insert(file,url,data)
    # remove as urls 404
    for listi in list:
        if 'https://www.papiron.com.br/perguntas/' in listi:
            id_url = listi[37:]
            if id_url not in ids:
                sitemap_delete(file,'https://www.papiron.com.br/perguntas/'+id_url)
    ####
    url_ultimas = 'https://www.papiron.com.br/perguntas/ultimas/ultimas_perguntas'
    xml_alterar_data(file,url_ultimas,data)

    return HttpResponse(status=200, content_type='text/xml')