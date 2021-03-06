# Generated by Django 3.1 on 2020-08-29 23:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_userprofile_followers'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='views',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='descriptionimage',
            name='article',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='main.article'),
        ),
        migrations.AddField(
            model_name='descriptionimage',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='image_uploader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='public',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='images',
            field=models.ManyToManyField(related_name='imgres', to='main.DescriptionImage'),
        ),
        migrations.AlterField(
            model_name='categories',
            name='image',
            field=models.ImageField(null=True, upload_to=main.models.categories, validators=[main.models.max_file_size]),
        ),
        migrations.AlterField(
            model_name='descriptionimage',
            name='image',
            field=models.ImageField(upload_to=main.models.article_image, validators=[main.models.max_file_size]),
        ),
        migrations.RemoveField(
            model_name='subforum',
            name='images',
        ),
        migrations.AddField(
            model_name='subforum',
            name='images',
            field=models.ImageField(null=True, upload_to=main.models.sub_forums, validators=[main.models.max_file_size]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(upload_to=main.models.profile_image, validators=[main.models.max_file_size]),
        ),
    ]
