# Generated by Django 3.1 on 2020-09-01 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20200830_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='description',
            field=models.TextField(max_length=4000),
        ),
        migrations.AlterField(
            model_name='article',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
