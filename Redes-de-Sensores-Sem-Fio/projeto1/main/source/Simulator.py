from Environment import Environment
from Parameter import Parameter

DEBUG = False


def debug(value):
    if DEBUG:
        print('<', value, '>', sep='')


def report(value):
    #print(value, end='')
    file = open('../results/out.txt', 'a')
    file.write(value)
    file.close()


def print_results(parameter, counter, results, more=''):
    clock, packets_transfer, packets_lost, nodes_founds, n_nodes, nodes_lost, energy_beg, energy_end = results
    report('\n\n# Cenário ' + str(counter) + '\n')
    report(more+'\n')
    report(str(parameter.descriptor) + '\n')
    report('\n')
    for i in range(84):
        report('-')
    report('\n')
    report('| {:^28} | {:^26} | {:^20} |\n'.format(
        'DESCRIÇÃO', 'VALOR', 'PORCENTAGEM'))
    for i in range(84):
        report('-')
    report('\n')
    report('| {:<28} | {:^26.2f} | {:^20} |\n'.format(
        'Tempo decorrido (em minutos)', clock / 60.0, ''))
    try:
        percent = packets_transfer * 100.0 / (packets_transfer + packets_lost)
    except ZeroDivisionError:
        percent = 0
    report('| {:<28} | {:^26} | {:^20.2f} |\n'.format(
        'Pacotes transferidos', packets_transfer, percent))
    try:
        percent = packets_lost * 100.0 / (packets_transfer + packets_lost)
    except ZeroDivisionError:
        percent = 0
    report('| {:<28} | {:^26} | {:^20.2f} |\n'.format(
        'Pacotes perdidos', packets_lost, percent))
    report('| {:<28} | {:^26} | {:^20.2f} |\n'.format(
        'Nós encontados pelo Sink', len(nodes_founds), len(nodes_founds) * 100.0 / n_nodes))
    report('| {:<28} | {:^26} | {:^20.2f} |\n'.format(
        'Nós descarregados', nodes_lost, nodes_lost * 100.0 / n_nodes))
    report('| {:<28} | {:^26} | {:^20.2f} |\n'.format(
        'Energia final da rede', energy_end, energy_end * 100.0 / energy_beg))
    for i in range(84):
        report('-')
    report('\n')


def execute_turn(parameter, strategy, turns, duty_cycle):
    n_nodes = parameter.number_node
    trans_range = parameter.trans_range  # meters
    speed_sink = parameter.speed_sink  # meters/second
    size_area = parameter.size_area  # area: meters²
    sink_route = list(parameter.sink_route)
    environment = Environment(n_nodes, trans_range, speed_sink, size_area, sink_route, strategy, duty_cycle)
    energy_begin = environment.energy_network_level()
    packets_transfer = 0
    packets_lost = 0
    nodes_founds = []
    nodes_lost = []
    clock = 0
    for i in range(turns):
        while not environment.end_sink_turn():
            pckt_trans, pckt_lost, n_founds, n_lost = environment.check_environment()
            packets_transfer += pckt_trans
            packets_lost += pckt_lost
            nodes_founds += n_founds
            nodes_lost += n_lost
            clock += 1
        environment.define_sink_route(list(parameter.sink_route), parameter.speed_sink)
    nodes_founds = set(nodes_founds)
    nodes_lost = environment.nodes_lost()
    energy_end = environment.energy_network_level()
    environment.finalize()
    return [clock, packets_transfer, packets_lost, nodes_founds, n_nodes, nodes_lost, energy_begin, energy_end]


def execute_scenarios(init, end, strategy, duty_cicle):
    parameter = Parameter()
    counter = init
    parameter.current = init - 1
    while parameter.current < end:
        results = execute_turn(parameter, strategy, 1, duty_cicle)
        more = 'Duty-cycle: '
        if duty_cicle:
            more += 'habilitado'
        else:
            more += 'desabilitado'
        print_results(parameter, counter, results, '')
        parameter.next()
        counter += 1


def main():
    scenario_list = Parameter().list_scenarios
    n_scenario = Parameter().scenarios
    strategy = Environment.NEAR
    duty_cicle = False
    while True:
        option = input('\nOpções:\n' +
                       '  1. Imprime cenários\n' +
                       '  2. Executar todos os cenários\n' +
                       '  3. Escolher cenários\n' +
                       '  4. Escolher número de visitas\n' +
                       '  5. Duty-cicle\n' +
                       '  0. Sair\n')
        if option == '0':
            exit()
        elif option == '1':
            print(scenario_list)
        elif option == '2':
            execute_scenarios(1, n_scenario, strategy, duty_cicle)
        elif option == '3':
            ok = False
            while not ok:
                start, end = input('Imprima intervalo de cenários: ').split()
                start, end = int(start), int(end)
                if start > end:
                    start, end = end, start
                if end <= n_scenario:
                    ok = True
                    execute_scenarios(start, end, strategy, duty_cicle)
        elif option == '4':
            turns = int(input('\nNúmero de visitas: '))
            print(scenario_list)
            scenario = int(input('\nCenário: '))
            parameter = Parameter()
            parameter.current = scenario - 1
            results = execute_turn(parameter, strategy, turns, duty_cicle)
            more = 'Número de viagens Sink: ' + str(turns) + '\n'
            #more += 'Duty-cycle: '
            #if duty_cicle:
            #    more += 'habilitado'
            #else:
            #    more += 'desabilitado'
            print_results(parameter, scenario, results, more)
        elif option == '5':
            if duty_cicle:
                dc = input('\nDesabilitar duty-cicle? [S/n]')
                if dc in ['s', 'S', '']:
                    duty_cicle = False
            else:
                dc = input('\nHabilitar duty-cicle? [S/n]')
                if dc in ['s', 'S', '']:
                    duty_cicle = True


if __name__ == '__main__':
    main()
