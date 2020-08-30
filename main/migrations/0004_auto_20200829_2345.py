# Generated by Django 3.1 on 2020-08-29 23:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0003_auto_20200829_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ManyToManyField(blank=True, related_name='categories', to='main.Categories'),
        ),
        migrations.AlterField(
            model_name='article',
            name='comments',
            field=models.ManyToManyField(blank=True, to='main.comment'),
        ),
        migrations.AlterField(
            model_name='article',
            name='dislikes',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='art_dislikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='article',
            name='forum',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='main.subforum'),
        ),
        migrations.AlterField(
            model_name='article',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='imgres', to='main.DescriptionImage'),
        ),
        migrations.AlterField(
            model_name='article',
            name='likes',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='art_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]