from django.shortcuts import render, get_object_or_404

def index(request):
    
    dados = {
        'perguntas' : 'TESTES'
    }
    return render(request,'index2.html', dados)


    
def teste(request):
    
    dados = {
        'perguntas' : 'TESTES'
    }
    return render(request,'index2.html', dados)

