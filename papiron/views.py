from django.shortcuts import render, HttpResponse

def index(request):
    
    return render(request,'index.html')

def sitemap(request):
    return HttpResponse(open('sitemap.xml').read(), content_type='text/xml')
    # return render (request,"sitemap.xml")