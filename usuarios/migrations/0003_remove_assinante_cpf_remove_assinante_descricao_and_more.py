# Generated by Django 4.1 on 2022-09-18 23:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_assinante_plano_alter_assinante_foto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assinante',
            name='CPF',
        ),
        migrations.RemoveField(
            model_name='assinante',
            name='descricao',
        ),
        migrations.RemoveField(
            model_name='assinante',
            name='email',
        ),
        migrations.RemoveField(
            model_name='assinante',
            name='facebook',
        ),
        migrations.RemoveField(
            model_name='assinante',
            name='foto',
        ),
        migrations.RemoveField(
            model_name='assinante',
            name='homepage',
        ),
        migrations.RemoveField(
            model_name='assinante',
            name='instagram',
        ),
        migrations.RemoveField(
            model_name='assinante',
            name='linkedIn',
        ),
        migrations.RemoveField(
            model_name='assinante',
            name='mensalidade',
        ),
        migrations.RemoveField(
            model_name='assinante',
            name='nome',
        ),
        migrations.RemoveField(
            model_name='assinante',
            name='plano',
        ),
        migrations.RemoveField(
            model_name='assinante',
            name='resumo',
        ),
        migrations.RemoveField(
            model_name='assinante',
            name='score',
        ),
        migrations.RemoveField(
            model_name='assinante',
            name='sobrenome',
        ),
        migrations.RemoveField(
            model_name='assinante',
            name='whatsapp',
        ),
        migrations.RemoveField(
            model_name='assinante',
            name='whatsapp_ddd',
        ),
        migrations.RemoveField(
            model_name='assinante',
            name='whatsapp_ddi',
        ),
        migrations.RemoveField(
            model_name='assinante',
            name='youtube',
        ),
    ]
