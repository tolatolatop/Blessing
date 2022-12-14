# Generated by Django 4.1.2 on 2022-10-23 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sns', '0002_search_modified_search_name_search_query'),
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=1024, unique=True)),
                ('date', models.DateTimeField()),
                ('content', models.TextField(blank=True)),
                ('t_id', models.IntegerField(unique=True)),
                ('username', models.CharField(max_length=128)),
                ('replyCount', models.IntegerField()),
                ('retweetCount', models.IntegerField()),
                ('likeCount', models.IntegerField()),
                ('quoteCount', models.IntegerField()),
                ('media', models.JSONField()),
                ('search', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sns.search')),
            ],
        ),
    ]
