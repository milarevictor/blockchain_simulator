# Generated by Django 2.2.3 on 2019-08-06 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='miner',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
