# Generated by Django 2.2.4 on 2019-08-17 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='calli',
            name='param4',
            field=models.CharField(blank=True, max_length=144),
        ),
        migrations.AddField(
            model_name='calli',
            name='param5',
            field=models.CharField(blank=True, max_length=144),
        ),
    ]
