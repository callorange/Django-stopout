# Generated by Django 2.0.2 on 2018-02-04 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webtoon', '0003_auto_20180204_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='created_date',
            field=models.DateField(null=True),
        ),
    ]
