# Generated by Django 2.2.3 on 2019-07-01 20:41

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('simulator', '0005_auto_20190701_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blockchain',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, help_text='ID único da blockchain.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, help_text='ID único do evento.', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, help_text='ID único do usuário.', primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='ID único do log.', primary_key=True, serialize=False)),
                ('time', models.FloatField(help_text='Tempo em que o log foi gerado.', null=True)),
                ('message', models.CharField(max_length=100, null=True)),
                ('blockchain', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='simulator.Blockchain')),
            ],
        ),
    ]
