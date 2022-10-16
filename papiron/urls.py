from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('admin_papiron428/', admin.site.urls),
    path('', views.index , name='index'),
    path('index/index1', views.index1 , name='index1'),
    path('perguntas/', include('perguntas.urls')), 
    path('usuarios/', include('usuarios.urls')), 
    path('sm/sitemap',views.sitemap,name='sitemap'),
    path('sitemap.xml',views.sitemap,name='sitemap'),
    path('robots.txt',views.robots,name='robots'),
    path('robot/Yudo7wmr4/gera_sitemap',views.gera_sitemap,name='gera_sitemap'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="usuarios/password/reset_senha.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="usuarios/password/reset_senha_envio.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="usuarios/password/reset_senha_confirmacao.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="usuarios/password/reset_senha_concluido.html"), name="password_reset_complete"),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 
from django.contrib.sitemaps.views import sitemap
path('sitemap.xml', sitemap, {'sitemaps': 'sitemaps'},
     name='django.contrib.sitemaps.views.sitemap')
path('sitemap2.xml', sitemap, {'sitemaps': 'sitemaps'},
     name='django.contrib.sitemaps.views.sitemap') 
path('sitemap', sitemap, {'sitemaps': sitemap},
 name='django.contrib.sitemaps.views.sitemap')