# Generated by Django 2.2.16 on 2021-08-16 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0008_auto_20210816_2022'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categories',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='genres',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='reviews',
            options={'ordering': ['-pub_date']},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['username']},
        ),
    ]
