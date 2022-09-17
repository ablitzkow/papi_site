# Generated by Django 4.1 on 2022-08-14 02:42

import datetime
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
            name='Pergunta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pergunta', models.TextField(max_length=2000)),
                ('comentario', models.TextField(blank=True, max_length=2000)),
                ('disciplina', models.CharField(max_length=150)),
                ('faculdade', models.CharField(max_length=150)),
                ('date_pergunta', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('publicada', models.BooleanField(default=False)),
                ('revisada', models.BooleanField(default=False)),
                ('pessoa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]