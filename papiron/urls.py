from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('admin_papiron428/', admin.site.urls),
    path('', views.index , name='index'),
    path('perguntas/', include('perguntas.urls')), 
    path('usuarios/', include('usuarios.urls')),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="usuarios/password/reset_senha.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="usuarios/password/reset_senha_envio.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="usuarios/password/reset_senha_confirmacao.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="usuarios/password/reset_senha_concluido.html"), name="password_reset_complete"),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib.sitemaps.views import sitemap
path('sitemap.xml', sitemap, {'sitemaps': 'sitemaps'},
     name='django.contrib.sitemaps.views.sitemap')