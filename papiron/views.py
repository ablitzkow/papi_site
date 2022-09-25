from django.shortcuts import render, HttpResponse

def index(request):
    
    return render(request,'index.html')

def sitemap(request):
    from . import settings
    return HttpResponse(open(str(settings.BASE_DIR)+'/papiron/sitemap.xml').read(), content_type='text/xml')