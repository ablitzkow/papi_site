# Generated by Django 4.1 on 2022-09-23 13:27

from django.db import migrations, models
import shortuuid.main


class Migration(migrations.Migration):

    dependencies = [
        ('perguntas', '0008_alter_pergunta_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pergunta',
            name='id',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, editable=False, max_length=22, primary_key=True, serialize=False),
        ),
    ]
