# Generated by Django 3.1 on 2020-08-29 23:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20200829_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='forum',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.subforum'),
        ),
    ]
