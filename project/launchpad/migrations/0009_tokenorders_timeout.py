# Generated by Django 2.1 on 2018-08-21 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('launchpad', '0008_auto_20180821_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='tokenorders',
            name='timeout',
            field=models.IntegerField(null=True),
        ),
    ]
