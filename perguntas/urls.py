from django.urls import path
from . import views


urlpatterns = [
    path('<str:id_url>', views.pergunta, name='pergunta'),
    path('ultimas/ultimas_perguntas', views.ultimas_perguntas, name='ultimas_perguntas'),
    path('analisar/analisar_perguntas', views.analisar_perguntas, name='analisar_perguntas'),
    path('analisar/publicar_perguntas', views.publicar_perguntas, name='publicar_perguntas'),
    path('ultimas/filtro_ultimas_perguntas', views.filtro_ultimas_perguntas, name='filtro_ultimas_perguntas'),
    path('search/buscar', views.buscar, name='buscar'),
    path('robot/w4Rt5i7pw/auto_publicar',views.auto_publicar, name='auto_publicar'),
    path('robot/w4Rt5i7pw/rodar',views.rodar, name='rodar'),

]