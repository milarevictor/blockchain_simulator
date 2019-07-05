from django.db import models
from django.urls import reverse
import uuid


class Simulation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='ID único da simulação.')
    name = models.CharField(max_length=100, null=True)

    blockchain = models.ForeignKey(
        'Blockchain', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, null=True)
    energyCost = models.FloatField(null=False, help_text='Custo em R$/kWh.')
    energyCons = models.FloatField(
        null=False, help_text='Gasto de energia em kW.')
    minersCP = models.FloatField(
        null=False, default=14, help_text='Poder computacional dos mineradores.')
    lambda_prob = models.FloatField(
        null=False, default=0.8, help_text='Média da distribuição probabilística.')

    def __str__(self):
        return f'{self.id}'


class Blockchain(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='ID único da blockchain.')
    avg_time = models.FloatField(
        null=False, help_text='Tempo médio para geração de novos blocos.')
    reward = models.FloatField(
        null=False, default=562505.875, help_text='Recompensa por minerar um bloco.')

    def get_num_info(self, time):
        num_miners = Event.objects.filter(blockchain=self).filter(
            typeOfEvent=3).filter(time__lte=time).count()
        blocks_add = Event.objects.filter(blockchain=self).filter(
            typeOfEvent=1).filter(time__lte=time).count()
        blocks_remove = Event.objects.filter(blockchain=self).filter(
            typeOfEvent=2).filter(time__lte=time).count()
        num_blocks = blocks_add - blocks_remove
        num_events = Event.objects.filter(
            blockchain=self).filter(time__lte=time).count()
        dados = {"num_miners": num_miners,
                 "num_blocks": num_blocks, "num_events": num_events}
        return dados

    def get_total_cp(self, time):
        totalCP = 0
        user = Simulation.objects.filter(blockchain=self)[0].user
        event_set = Event.objects.filter(blockchain=self).filter(
            typeOfEvent=3).filter(time__lte=time)
        for event in event_set:
            miner = event.miner
            totalCP += miner.computPower
        return totalCP + user.computPower


class Block(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='ID único do bloco.')
    blockchain = models.ForeignKey(
        'Blockchain', on_delete=models.CASCADE, null=False)


class Event(models.Model):
    event_id = models.IntegerField(
        null=True, default=1, help_text='ID único do evento.')
    event_choices = ((1, 'Adição de bloco.'), (2, 'Exclusão de bloco.'),
                     (3, 'Inserção de minerador.'), (4, 'Exclusão de minerador.'))
    time = models.FloatField(
        null=False, help_text='Tempo em que ocorreu o evento.')
    typeOfEvent = models.IntegerField(
        null=False, choices=event_choices, help_text='Tipo de evento.')
    blockchain = models.ForeignKey(
        'Blockchain', on_delete=models.CASCADE, null=False)
    miner = models.ForeignKey('Miner', on_delete=models.CASCADE, null=True)
    block = models.ForeignKey('Block', on_delete=models.CASCADE, null=True)


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='ID único do usuário.')
    computPower = models.FloatField(
        null=True, help_text='Poder computacional do usuário.')


class Miner(models.Model):
    computPower = models.FloatField(
        null=False, help_text='Poder computacional do minerador.')
    blockchain = models.ForeignKey(
        'Blockchain', on_delete=models.CASCADE, null=True)


class Log(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='ID único do log.')
    blockchain = models.ForeignKey(
        'Blockchain', on_delete=models.CASCADE, null=True)
    event_id = models.FloatField(null=True, help_text='ID do evento.')
    message = models.CharField(max_length=100, null=True)
