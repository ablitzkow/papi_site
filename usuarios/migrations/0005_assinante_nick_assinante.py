# Generated by Django 4.1 on 2022-09-19 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_remove_assinante_nick_assinante'),
    ]

    operations = [
        migrations.AddField(
            model_name='assinante',
            name='nick_assinante',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
