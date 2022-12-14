# Generated by Django 4.1 on 2022-09-17 22:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Registro_Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_register', models.CharField(max_length=200)),
                ('code_sent', models.IntegerField()),
                ('data_code', models.DateField()),
                ('approve_code', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Assinante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # ('email', models.CharField(max_length=200)),
                # ('nome', models.CharField(max_length=200)),
                # ('sobrenome', models.CharField(max_length=200)),
                # ('mensalidade', models.BooleanField(default=False)),
                # ('CPF', models.CharField(max_length=200)),
                # ('instagram', models.CharField(blank=True, max_length=200)),
                # ('whatsapp_ddi', models.CharField(default='+55', max_length=3)),
                # ('whatsapp_ddd', models.CharField(blank=True, max_length=3)),
                # ('whatsapp', models.CharField(blank=True, max_length=25)),
                # ('linkedIn', models.CharField(blank=True, max_length=300)),
                # ('facebook', models.CharField(blank=True, max_length=300)),
                # ('youtube', models.CharField(blank=True, max_length=300)),
                # ('homepage', models.CharField(blank=True, max_length=300)),
                # ('descricao', models.CharField(blank=True, max_length=2500)),
                # ('resumo', models.CharField(blank=True, max_length=250)),
                # ('plano' , models.CharField(max_length=300,blank=True)),
                # ('score', models.IntegerField(blank=True, default=0)),
                # ('foto', models.ImageField(blank=True, default='/media/usuarios/no-image.png', upload_to='media/usuarios/')),
                ('assinante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
