# Generated by Django 2.2.16 on 2021-08-18 19:32

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата добавления')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.RemoveField(
            model_name='comments',
            name='author',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='review',
        ),
        migrations.AlterModelOptions(
            name='categories',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='genres',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-pub_date']},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['username']},
        ),
        migrations.RenameField(
            model_name='review',
            old_name='created',
            new_name='pub_date',
        ),
        migrations.RemoveField(
            model_name='review',
            name='rating',
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('author', 'title'), name='unique_reviews'),
        ),
        migrations.DeleteModel(
            name='Comments',
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='reviews.Review'),
        ),
    ]
