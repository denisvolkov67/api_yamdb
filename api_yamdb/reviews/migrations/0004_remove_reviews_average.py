# Generated by Django 2.2.6 on 2021-08-14 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20210814_1843'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviews',
            name='average',
        ),
    ]
