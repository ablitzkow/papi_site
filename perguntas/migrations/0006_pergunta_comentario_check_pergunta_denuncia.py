# Generated by Django 4.1 on 2022-09-20 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perguntas', '0005_rename_date_comentario_comentario_data_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='pergunta',
            name='comentario_check',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pergunta',
            name='denuncia',
            field=models.BooleanField(default=False),
        ),
    ]
 