# Generated by Django 3.2.3 on 2022-08-17 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0006_assinante_descricao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assinante',
            name='descricao',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='assinante',
            name='facebook',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='assinante',
            name='instagram',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='assinante',
            name='linkedIn',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='assinante',
            name='whatsapp',
            field=models.CharField(blank=True, max_length=25),
        ),
    ]
