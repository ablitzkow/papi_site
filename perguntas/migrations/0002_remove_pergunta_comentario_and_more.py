# Generated by Django 4.1 on 2022-09-18 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('perguntas', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pergunta',
            name='comentario', 
        ),
        migrations.RemoveField(
            model_name='pergunta',
            name='email_comentario',
        ),
        migrations.RemoveField(
            model_name='pergunta',
            name='revisao_qtd',
        ),
        migrations.RemoveField(
            model_name='pergunta',
            name='revisao_solicitada',
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_comentario', models.CharField(blank=True, max_length=200)),
                ('comentario', models.TextField(blank=True, max_length=2500)),
                ('revisao_solicitada', models.BooleanField(default=False)),
                ('revisao_qtd', models.IntegerField(default=0)),
                ('id_pergunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='perguntas.pergunta')),
            ],
        ),
    ]
