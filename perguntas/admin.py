from django.contrib import admin
from .models import Comentario,Pergunta,Revisao,LikeBtn

class ListandoPerguntas(admin.ModelAdmin):
    list_display = ('id', 'id_url' , 'pageviews' ,'faculdade', 'disciplina' , 'publicada', 'comentario_check','denuncia','listada')
    list_display_links = ('id', 'id_url' , 'faculdade', 'disciplina')
    search_fields = ('pergunta','id','id_url')
    list_filter = ('faculdade','disciplina','denuncia', 'publicada','listada')
    list_editable = ('publicada', 'comentario_check','denuncia','listada')
    list_per_page = 50

class ListandoComentarios(admin.ModelAdmin):
    list_display = ('id', 'id_pergunta' ,'comentario','email','revisao_qtd','revisao_solicitada')
    list_display_links = ('id',  'id_pergunta' ,'comentario')

class ListandoRevisoes(admin.ModelAdmin):
    list_display = ('id', 'id_pergunta', 'email','revisao')
    list_display_links = ('id', 'id_pergunta')
    search_fields = ['id_pergunta__id'] #ótimo search
    list_per_page = 20

class ListandoLikes(admin.ModelAdmin):
    list_display = ('id', 'id_pergunta','user','likes')
    list_display_links = ('id', 'id_pergunta','user')

admin.site.register(Pergunta, ListandoPerguntas)
admin.site.register(Revisao, ListandoRevisoes)
admin.site.register(LikeBtn, ListandoLikes)
admin.site.register(Comentario, ListandoComentarios)
