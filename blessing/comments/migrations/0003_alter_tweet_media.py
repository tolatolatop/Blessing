# Generated by Django 4.1.2 on 2022-10-23 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_tweet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='media',
            field=models.JSONField(null=True),
        ),
    ]
