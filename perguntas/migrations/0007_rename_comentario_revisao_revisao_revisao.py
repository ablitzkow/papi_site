# Generated by Django 4.1 on 2022-09-20 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perguntas', '0006_pergunta_comentario_check_pergunta_denuncia'),
    ]

    operations = [
        migrations.RenameField(
            model_name='revisao',
            old_name='comentario_revisao',
            new_name='revisao',
        ),
    ]
