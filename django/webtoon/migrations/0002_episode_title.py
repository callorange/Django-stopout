# Generated by Django 2.0.2 on 2018-02-04 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webtoon', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='title',
            field=models.CharField(default='', max_length=200),
        ),
    ]
