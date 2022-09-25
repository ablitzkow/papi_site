from django.urls import path
from . import views
from . import forms

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('dados_cadastro', views.dados_cadastro, name='dados_cadastro'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('meus_dados', views.meus_dados, name='meus_dados'),
    path('minhas_perguntas', views.minhas_perguntas, name='minhas_perguntas'),
    # path('<int:pergunta_id>', views.ver_minha_colaboracao, name='ver_minha_colaboracao'),
    path('meus_comentarios', views.meus_comentarios, name='meus_comentarios'),
    path('meu_perfil', views.meu_perfil, name='meu_perfil'),
    path('form/pergunta', forms.form_pergunta, name='form_pergunta'),
    path('form/dados', views.form_dados, name='form_dados'),
    path('form/comentar', views.form_comentar, name='form_comentar'),
    # path('cadastro_email', views.cadastro_email, name='cadastro_email'),
    path('form/cadastro', forms.cadastro, name='cadastro'),
    path('form/email_code', forms.form_email_code, name='form_email_code'),
    path('revisar', views.revisar, name='revisar'),
    path('curtir', views.curtir, name='curtir'),
    path('form/revisar', views.form_revisar, name='form_revisar'),
    path('perfil/<str:id_perfil>', views.perfil, name='perfil'),
    path('planos', views.planos, name='planos'),
    path('assessores', views.assessores, name='assessores'),
    path('incluir_assinante', forms.incluir_assinante, name='incluir_assinante'),
    path('form_incluir_assinante',forms.form_incluir_assinante, name = 'form_incluir_assinante'),
    path('captcha', forms.captcha, name = 'captcha'),

]