# Generated by Django 4.1 on 2022-09-05 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_curso_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='curso',
            name='completo',
            field=models.BooleanField(default=False),
        ),
    ]
