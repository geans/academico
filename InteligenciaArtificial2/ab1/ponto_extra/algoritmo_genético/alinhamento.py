"""
Goal: maximize the equation αx+βy+δz
αβδ are floats pass in firts line separeted for space
The other lines are the set of dna.

Input Format example:

0.7 0.85 0.9
AATC
CT
TAC

... (set formated of alphabet 'ATGC')
"""
from random import randint, choice
from time import time
from sys import argv

if len(argv) < 2:
    print("Mode use:\n\t{} <time_limit_in_secods>".format(argv[0]))
    exit()
else:
    time_limit = int(argv[1])
   
def mdebug(value, end='\n'):
    if __name__ == '__main__':
        print(value, end = end)

# Defines
nucleic_acid = 'ATGC'
gap = '-'
randbool = lambda: choice([True, False])
randlist = lambda list: choice(list)
chance_for_adapted_minor = 1  # 1%, 1-100
chance_of_mutation = 1  # 1%, 1-100
history_file_name = 'history.log'


def fix_gaps(population):
    population_fixed_gap = []
    for chromosome in population:
        with_string_gap = True
        for j in range(len(chromosome[0])):
            if with_string_gap:  # remove initials gaps
                for i in range(len(chromosome)):
                    if chromosome[i][j] == False:  # False is not a gap
                        with_string_gap = False
                        break
                if with_string_gap:
                    for h in range(len(chromosome)):  # remove first position
                        chromosome[h][j] = False
            population_fixed_gap += [chromosome]
    return population_fixed_gap


def build_alignment(input_source, population):
    aligned = []
    for chromosome in population:
        if len(chromosome) != len(input_source):
            mdebug('Diff between size of chromosome and input_source:')
            mdebug('{} != {}'.format(len(chromosome), len(input_source)))
            raise
        max_line_size = 0
        chromosome_dna = []
        for i in range(len(chromosome)):
            tmp_dna = input_source[i]
            chromosome_dna_line = []
            for gene in chromosome[i]:
                if gene:  # True is a gap
                    chromosome_dna_line += gap
                else:
                    try:  # the length of the dna_tmp may end
                        chromosome_dna_line += tmp_dna[0]
                        tmp_dna = tmp_dna[1:]
                    except Exception:
                        pass
            chromosome_dna_line += tmp_dna  # if tmp_dna is empty, then no problem
            if len(chromosome_dna_line) > max_line_size:
                max_line_size = len(chromosome_dna_line)
            chromosome_dna += [chromosome_dna_line]
        filled = []
        for c in chromosome_dna:
            line_filled = c
            for i in range(max_line_size - len(c)):
                line_filled += gap
            filled += [line_filled]
        aligned += [filled]
    return aligned


def get_features(individual_aligned):
    x,y,z = 0,0,0
    p_size = len(individual_aligned)
    for i in range(p_size):
        for j in range(i+1, p_size):
            dna1, dna2 = individual_aligned[i], individual_aligned[j]
            min_size = min(len(dna1), len(dna2))
            for h in range(min_size):
                if dna1[h] == dna2[h]:
                    if dna1[h] == gap: z += 1
                    else:              x += 1
                else:
                    y += 1
            dna = dna1 if len(dna1) > len(dna2) else dna2
            for h in range(max(len(dna1), len(dna2)) - min_size):
                if dna[h] == gap: z += 1
                else:             y += 1
    return x,y,z

    
def build_new_population(parents, population_size):
    new_population = parents
    count = 0
    while len(new_population) < population_size and count < (population_size << 1):
        count += 1
        parent_a, parent_b = randlist(parents), randlist(parents)
        if parent_a == parent_b:
            parent_b = randlist(parents)
        chromosome_size = len(parent_b)
        chromosome_line_size = len(parent_b[0])
        child_a = []
        child_b = []
        for i in range(len(parent_a)):
            cut_point = randint(1, chromosome_line_size - 1)
            child_a += [parent_a[i].copy()[:cut_point] + parent_b[i].copy()[cut_point:]]
            child_b += [parent_b[i].copy()[:cut_point] + parent_a[i].copy()[cut_point:]]
        children = [child_a, child_b]
        if child_a in new_population:
            children.remove(child_a)
        if child_b in new_population:
            children.remove(child_b)
        if children == []:
            continue
        
        if randint(1,100) <= chance_of_mutation:
            mutant = randlist(children)
            children.remove(mutant)
            i = randint(0, chromosome_size-1)
            j = randint(0, len(mutant[i])-1)
            mutant[i][j] = not mutant[i][j]
            children.append(mutant)
        
        new_population += children
    number_of_lines = len(new_population[0])
    size_line = len(new_population[0][0])
    if len(new_population) < population_size:
        # generate random population
        new_individual = []
        for i in range(number_of_lines):
            line = [randbool() for h in range(size_line)]
            new_individual += [line]
        new_population += [new_individual]
    new_population = new_population[:population_size]  # case have one more
    return new_population


class HandleAlign:
    def __init__(self, individual, x,y,z, a,b,d, chromosome):
        self.individual = individual
        self.x = x
        self.y = y
        self.z = z
        self.a = a
        self.b = b
        self.d = d
        self.chromosome = chromosome
        self.score = a*x + b*y + d*z
    
    def copy(self):
        return HandleAlign(self.individual.copy(),
                           int(self.x),int(self.y),int(self.z),
                           float(self.a),float(self.b),float(self.d), self.chromosome.copy())
        


def print_log(generation, population):
    msg =  'Generation: {}\n'.format(generation)
    msg += 'Population:\n'
    count = 0
    for matrix in population:
        count += 1
        msg += '\nIndividual ' + str(count) + ':\n'
        for line in matrix:
            for gap in line:
                msg += '-' if gap else '.'
            msg += '\n'
    log = open(history_file_name, '+a')
    log.write(msg)
    log.flush()
    log.close()

def main():
    # Input #
    alpha, beta, delta = input().split()  # read weights
    alpha, beta, delta = float(alpha), float(beta), float(delta)
    dna = input()
    input_source = []
    max_size = 0
    while dna:  # read lines with dna
        if len(dna) > max_size:
            max_size = len(dna)
        input_source += [dna]
        try:
            dna = input()
        except Exception:
            break
    # End input #
            
    chromosome_size = max_size
    population_size = 10

    # Initial population (random) #
    population = []
    dna_population = []
    number_of_lines = len(input_source)
    for i in range(population_size):
        chromosome = []  # chromosome
        for j in range(number_of_lines):
            chromosome_part = [randbool() for h in range(chromosome_size)]
            chromosome += [chromosome_part]
        population += [chromosome]
    # End initial population (random) #

    mdebug('| {:^10} | {:^10} | {:^10} | {:^10} |'.format('Progress', 'Generation', 'Better', 'Worse'))
    more_adapted_handle = None
    less_adapted_handle = None
    generation = 0
    erase_file = open(history_file_name, 'w')
    erase_file.close()
    time_for_better = 0
    start_time = time()
    while time() - start_time < time_limit:
        generation += 1
        population = fix_gaps(population)
        print_log(generation, population)
        population_aligned = build_alignment(input_source, population)
        if len(population_aligned) != len(population):
            mdebug('Diff between size of population_aligned and population:')
            mdebug('{} != {}'.format(len(population_aligned), len(population)))
            raise
        
        vector_handle = []
        for i in range(len(population_aligned)):
            x,y,z = get_features(population_aligned[i])
            handle = HandleAlign(population_aligned[i], x,y,z, alpha,beta,delta, population[i])
            vector_handle += [handle]
        
        adaptation = sorted(vector_handle, key=lambda x: x.score, reverse=True)
        more_adapted_size = population_size >> 1
        more_adapted = adaptation[:more_adapted_size]
        if randint(1,100) <= chance_for_adapted_minor:
            # lottery of less adapted
            try:
                new = randlist(adaptation[more_adapted_size:])
            except Exception:
                mdebug('adaptation length:', len(adaptation))
                mdebug('pivot:', more_adapted_size)
                mdebug('population length:', len(population))
                mdebug(population)
                raise
            # lottery one from more adapted
            out = randlist(more_adapted)
            more_adapted.remove(out)
            more_adapted.append(new)
            more_adapted = sorted(more_adapted, key=lambda x: x.score, reverse=True)
        more_adapted_population = [handle.chromosome for handle in more_adapted]  #!!! use chromosome and not individual !!!
        population = build_new_population(more_adapted_population, population_size)
        try:
            if more_adapted_handle.score < more_adapted[0].score:
                time_for_better = time() - start_time
        except Exception:
            pass
        more_adapted_handle = more_adapted[0]
        less_adapted_handle = adaptation[-1]
        mdebug('| {:>9.0f}% | {:>10} | {:^10.2f} | {:^10.2f} |'.format(
              (time() - start_time)*100/time_limit, generation, more_adapted_handle.score, less_adapted_handle.score), end='\r')
    
    mdebug('\n\n')
    mdebug('More adapted: {:.2f}'.format(more_adapted_handle.score))
    mdebug('x:{:<5} y:{:<5} z:{:<5}'.format(more_adapted_handle.x, more_adapted_handle.y, more_adapted_handle.z))
    for line in more_adapted_handle.individual:
        mdebug(''.join(line))
    for line in more_adapted_handle.chromosome:
        mdebug(line)
    
    mdebug('\n')
    mdebug('Less adapted: {:.2f}'.format(less_adapted_handle.score))
    mdebug('x:{:<5} y:{:<5} z:{:<5}'.format(less_adapted_handle.x, less_adapted_handle.y, less_adapted_handle.z))
    for line in less_adapted_handle.individual:
        mdebug(''.join(line))
    for line in less_adapted_handle.chromosome:
        mdebug(line)

    mdebug('')
    mdebug('{:^7} {:^7} {:^7}'.format('alpha', 'beta', 'delta'))
    mdebug('{:^7} {:^7} {:^7}'.format(alpha, beta, delta))
    
    mdebug('\nTime for maximize score: {:.2f} seconds'.format(time_for_better))

    return more_adapted_handle

if __name__ == '__main__':
    main()