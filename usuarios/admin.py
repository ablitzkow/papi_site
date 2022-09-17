from django.contrib import admin

from .models import Assinante,  Registro_Email

class ListandoColaboradores(admin.ModelAdmin):
    list_display = ('id', 'assinante', 'mensalidade', 'CPF' , 'whatsapp','score')
    list_display_links = ('id', 'assinante',)
    search_fields = ('assinante',)
    list_filter = ('mensalidade',)
    list_editable = ('mensalidade',)
    list_per_page = 20


class ListandoCode(admin.ModelAdmin):
    list_display = ('id', 'email_register', 'code_sent', 'data_code' , 'approve_code')
    list_display_links = ('id', 'email_register',)

admin.site.register(Assinante, ListandoColaboradores)
admin.site.register(Registro_Email, ListandoCode)
