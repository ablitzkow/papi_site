from django.contrib import admin

from .models import Assinante,  Registro_Email , Especialidade , Stat_WhatsApp

class ListandoColaboradores(admin.ModelAdmin):
    list_display = ('id', 'id_perfil', 'assinante', 'mensalidade', 'CPF' , 'whatsapp','score')
    list_display_links = ('id', 'id_perfil', 'assinante',)
    search_fields = ('assinante',)
    list_filter = ('mensalidade',)
    list_editable = ('mensalidade',)
    list_per_page = 20


class ListandoCode(admin.ModelAdmin):
    list_display = ('id', 'email_register', 'code_sent', 'data_code' , 'approve_code')
    list_display_links = ('id', 'email_register',)

class ListandoEspecialidade(admin.ModelAdmin):
    list_display = ('id', 'assinante', 'faculdade', 'disciplina','peso')
    list_display_links = ('id', 'assinante', 'faculdade',)
    list_filter = ('faculdade', 'disciplina','assinante')
    list_editable = ('disciplina','peso')

class ListandoStat_WhatsApp(admin.ModelAdmin):
    list_display = ('id', 'assinante', 'data', 'id_url')
    list_display_links = ('id', 'assinante', 'data', 'id_url')

admin.site.register(Assinante, ListandoColaboradores)
admin.site.register(Registro_Email, ListandoCode)
admin.site.register(Especialidade, ListandoEspecialidade)
admin.site.register(Stat_WhatsApp, ListandoStat_WhatsApp)