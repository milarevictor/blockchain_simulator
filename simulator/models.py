from django.db import models
from django.urls import reverse
import uuid


class Simulation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='ID único da simulação.')
    blockchain = models.ForeignKey(
        'Blockchain', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, null=True)
    energyCost = models.FloatField(null=False, help_text='Custo em R$/kWh.')
    energyCons = models.FloatField(
        null=False, help_text='Gasto de energia em kW.')

    def __str__(self):
        return f'{self.id}'


class Blockchain(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='ID único da blockchain.')
    avg_time = models.FloatField(
        null=False, help_text='Tempo médio para geração de novos blocos.')

    def get_num_info(self, time):
        num_miners = Event.objects.filter(blockchain=self).filter(
            typeOfEvent=3).filter(time__lte=time).count()
        blocks_add = Event.objects.filter(blockchain=self).filter(
            typeOfEvent=1).filter(time__lte=time).count()
        blocks_remove = Event.objects.filter(blockchain=self).filter(
            typeOfEvent=2).filter(time__lte=time).count()
        num_blocks = blocks_add - blocks_remove
        dados = {"num_miners": num_miners, "num_blocks": num_blocks}
        return dados

    def get_total_cp(self):
        totalCP = 0
        miners_set = Miner.objects.filter(blockchain=self.id)
        for miner in miners_set:
            totalCP += miner.computPower
        return totalCP


class Block(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='ID único do bloco.')
    blockchain = models.ForeignKey(
        'Blockchain', on_delete=models.CASCADE, null=False)


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='ID único do evento.')
    event_choices = ((1, 'Adição de bloco.'), (2, 'Exclusão de bloco.'),
                     (3, 'Inserção de minerador.'), (4, 'Exclusão de minerador.'))
    time = models.FloatField(
        null=False, help_text='Tempo em que ocorreu o evento.')
    typeOfEvent = models.IntegerField(
        null=False, choices=event_choices, help_text='Tipo de evento.')
    blockchain = models.ForeignKey(
        'Blockchain', on_delete=models.CASCADE, null=False)
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
    time = models.FloatField(
        null=True, help_text='Tempo em que o log foi gerado.')
    message = models.CharField(max_length=100, null=True)
