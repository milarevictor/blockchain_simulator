# Generated by Django 2.2.3 on 2019-07-05 16:22

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='ID único do bloco.', primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Blockchain',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='ID único da blockchain.', primary_key=True, serialize=False)),
                ('avg_time', models.FloatField(help_text='Tempo médio para geração de novos blocos.')),
                ('reward', models.FloatField(default=562505.875, help_text='Recompensa por minerar um bloco.')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='ID único do usuário.', primary_key=True, serialize=False)),
                ('computPower', models.FloatField(help_text='Poder computacional do usuário.', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Simulation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='ID único da simulação.', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, null=True)),
                ('energyCost', models.FloatField(help_text='Custo em R$/kWh.')),
                ('energyCons', models.FloatField(help_text='Gasto de energia em kW.')),
                ('minersCP', models.FloatField(default=14, help_text='Poder computacional dos mineradores.')),
                ('lambda_prob', models.FloatField(default=0.8, help_text='Média da distribuição probabilística.')),
                ('blockchain', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='simulator.Blockchain')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='simulator.User')),
            ],
        ),
        migrations.CreateModel(
            name='Miner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('computPower', models.FloatField(help_text='Poder computacional do minerador.')),
                ('blockchain', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='simulator.Blockchain')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='ID único do log.', primary_key=True, serialize=False)),
                ('event_id', models.FloatField(help_text='ID do evento.', null=True)),
                ('message', models.CharField(max_length=100, null=True)),
                ('blockchain', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='simulator.Blockchain')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.IntegerField(default=1, help_text='ID único do evento.', null=True)),
                ('time', models.FloatField(help_text='Tempo em que ocorreu o evento.')),
                ('typeOfEvent', models.IntegerField(choices=[(1, 'Adição de bloco.'), (2, 'Exclusão de bloco.'), (3, 'Inserção de minerador.'), (4, 'Exclusão de minerador.')], help_text='Tipo de evento.')),
                ('block', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='simulator.Block')),
                ('blockchain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simulator.Blockchain')),
                ('miner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='simulator.Miner')),
            ],
        ),
        migrations.AddField(
            model_name='block',
            name='blockchain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='simulator.Blockchain'),
        ),
    ]
