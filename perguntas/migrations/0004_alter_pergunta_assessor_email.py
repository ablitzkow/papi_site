# Generated by Django 3.2.3 on 2022-08-21 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perguntas', '0003_pergunta_assessor_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pergunta',
            name='assessor_email',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
