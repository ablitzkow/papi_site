from django.contrib import admin
from .models import Pergunta,Revisao,LikeBtn

class ListandoPerguntas(admin.ModelAdmin):
    list_display = ('id', 'pergunta', 'faculdade', 'disciplina' , 'publicada')
    list_display_links = ('id', 'pergunta')
    search_fields = ('pergunta','id')
    list_filter = ('faculdade',)
    list_editable = ('publicada',)
    list_per_page = 10

class ListandoRevisoes(admin.ModelAdmin):
    list_display = ('id', 'id_pergunta', 'revisor_email','comentario_revisao')
    list_display_links = ('id', 'id_pergunta','comentario_revisao')
    search_fields = ['id_pergunta__id'] #ótimo search
    list_per_page = 20

class ListandoLikes(admin.ModelAdmin):
    list_display = ('id', 'id_pergunta','user','likes')
    list_display_links = ('id', 'id_pergunta','user')

admin.site.register(Pergunta, ListandoPerguntas)
admin.site.register(Revisao, ListandoRevisoes)
admin.site.register(LikeBtn, ListandoLikes)
