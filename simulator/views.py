from django.shortcuts import render
from simulator.models import Simulation, Blockchain, Block, Event, User, Miner, Log
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from simulator.forms import createSimulForm
from django.http import JsonResponse
import datetime
import math
import numpy as np


def createSimul(request):
    form = createSimulForm()
    return render(request, 'simulator/createSimul.html', context={'form': form})


def start_simul(request):
    if request.is_ajax():
        simulation_id = request.GET['sid']
        # Ainda não configurei o log por evento
        # event_id = request.GET['eid']
        time = request.GET['t']
        button = request.GET['operation']
        simulation = Simulation.objects.get(id=simulation_id)
        blockchain = simulation.blockchain
        log_set = []
        latest_time = Event.objects.filter(
            blockchain=blockchain).latest('time').time
        if button == 'next_time':
            log = ''
            while int(time) > latest_time:
                generate_events(10, simulation, latest_time)
                latest_time = Event.objects.filter(
                    blockchain=blockchain).latest('time').time
            logs = Log.objects.filter(
                blockchain=blockchain).filter(time__lte=time)
            for log in logs:
                log_set.append(log.message)
        dados = simulation.blockchain.get_num_info(time=time)
        dados['log'] = log_set
        return JsonResponse(dados)
    # Os próximos dados entrarão via post (formulário)
    avg_time = 10
    energCost = 9
    energCons = 8
    ownCP = 0.8
    # A partir daqui crio a blockchain, simulação, usuário e seto o primeiro minerador
    blockchain = Blockchain(avg_time=avg_time)
    blockchain.save()
    user = User(computPower=ownCP)
    user.save()
    simulation = Simulation(blockchain=blockchain,
                            energyCons=energCons, energyCost=energCost, user=user)
    simulation.save()
    start_miner = Miner(blockchain=blockchain, computPower=20.0)
    start_miner.save()
    event = Event(time=0, typeOfEvent=3,
                  blockchain=blockchain)
    event.save()
    message = 'Log(time=' + str(0) + 'min): Inserção de minerador.'
    log = Log(time=0, blockchain=simulation.blockchain,
              message=message)
    log.save()
    num_dados = generate_events(0, simulation)

    dados = {"simulation_id": f'{simulation.id}',
             "blockchain_id": f'{blockchain.id}',
             "num_miners": num_dados['num_miners'],
             "num_blocks": num_dados['num_blocks']}
    return render(request, 'simulator/index.html', context=dados)


def generate_events(num_events, simulation, time=0):
    events = 0
    # O valor do minerCP tá setado manualmente, virá do formulário depois
    minerCP = 20.0
    userCP = simulation.user.computPower
    totalCP = simulation.blockchain.get_total_cp()
    avg_time = simulation.blockchain.avg_time
    dificuldade = totalCP*avg_time*60
    while events < num_events:
        time += 1
        try:
            block_time = Event.objects.filter(
                blockchain=simulation.blockchain).filter(typeOfEvent=1).latest('time').time
        except:
            block_time = 0
        time_interval = time - block_time
        # Abaixo eu defini o lambda de Poisson como 0.3
        miners_entered = np.random.poisson(0.3, 1)[0]
        prob = 1 - math.exp(-1*userCP*time_interval*3600/dificuldade)
        if prob > 0.5:
            block = Block(blockchain=simulation.blockchain)
            block.save()
            event = Event(time=time, typeOfEvent=1,
                          blockchain=simulation.blockchain, block=block)
            event.save()
            message = 'Log(time=' + str(time) + 'min): Inserção de bloco.'
            log = Log(time=time, blockchain=simulation.blockchain,
                      message=message)
            log.save()
            events += 1
        for i in range(miners_entered):
            miner = Miner(blockchain=simulation.blockchain,
                          computPower=minerCP)
            miner.save()
            event = Event(time=time, typeOfEvent=3,
                          blockchain=simulation.blockchain)
            event.save()
            message = 'Log(time=' + str(time) + 'min): Inserção de minerador.'
            log = Log(time=time, blockchain=simulation.blockchain,
                      message=message)
            log.save()
            events += 1
    return simulation.blockchain.get_num_info(time)
