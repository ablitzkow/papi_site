from django.urls import path
from . import views


urlpatterns = [
    path('<str:pergunta_id>', views.pergunta, name='pergunta'),
    path('ultimas/ultimas_perguntas', views.ultimas_perguntas, name='ultimas_perguntas'),
    path('ultimas/filtro_ultimas_perguntas', views.filtro_ultimas_perguntas, name='filtro_ultimas_perguntas'),
    path('buscar', views.buscar, name='buscar'),
]