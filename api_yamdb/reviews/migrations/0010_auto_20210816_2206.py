# Generated by Django 2.2.16 on 2021-08-16 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0009_auto_20210816_2204'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Reviews',
            new_name='Review',
        ),
    ]
