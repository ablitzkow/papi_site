# Generated by Django 4.1 on 2022-10-09 21:18

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0009_especialidade'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stat_WhatsApp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('id_url', models.CharField(max_length=22)),
                ('assinante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.assinante')),
            ],
        ),
    ]
