# Generated by Django 4.1 on 2022-09-20 12:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perguntas', '0004_comentario_date_comentario'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comentario',
            old_name='date_comentario',
            new_name='data',
        ),
        migrations.RenameField(
            model_name='comentario',
            old_name='email_comentario',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='comentario',
            old_name='nick_comentario',
            new_name='nick',
        ),
        migrations.RenameField(
            model_name='pergunta',
            old_name='date_pergunta',
            new_name='data',
        ),
        migrations.RenameField(
            model_name='pergunta',
            old_name='email_pergunta',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='pergunta',
            old_name='nick_pergunta',
            new_name='nick',
        ),
        migrations.RenameField(
            model_name='revisao',
            old_name='email_revisor',
            new_name='email',
        ),
    ]
