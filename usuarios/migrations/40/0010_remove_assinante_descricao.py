# Generated by Django 3.2.3 on 2022-08-17 22:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0009_assinante_descricao'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assinante',
            name='descricao',
        ),
    ]
