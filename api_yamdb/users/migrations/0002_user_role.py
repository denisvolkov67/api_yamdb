# Generated by Django 2.2.16 on 2021-08-09 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.TextField(blank=True, verbose_name='Роль пользователя'),
        ),
    ]
