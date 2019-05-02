import random

MAX_WEIGHT = 12
MAX_VOLUME= 10

VAL = 0
WEIGHT = 1
VOLUME=2

NUM_GENERATIONS = 10000
NUM_TESTS = 5

GENERATION_SIZE = 10
CROSSOVER_RATE = 0.7
MUTATION_RATE = 0.01

CHROMOSOME_SIZE = 0

inventory = []

chromosomes = []
fitness = []
sum_fitness = 0

START_POP_WITH_ZEROES = False

### LOGISTIC FUNCTIONS ###
def read_file():
    global CHROMOSOME_SIZE

    with open("Inventory") as f:
        lines = f.readlines()

    for line in lines:
        line = line.split("\t")
        inventory.append((line[0], line[1], line[2].replace("\n", "")))

    CHROMOSOME_SIZE = len(inventory)


def generate_base_generation():
    chromosome = ""
    for i in range(GENERATION_SIZE):
        for j in range(CHROMOSOME_SIZE):
            chromosome += str(random.randint(0, 1))
        chromosomes.append(chromosome)
        chromosome = ""
    print("Initial Population:",chromosomes)


def test_fitness():
    global fitness
    global sum_fitness

    weight = 0
    value = 0
    volume=0

    for i in range(GENERATION_SIZE):
        chromosome = chromosomes[i]
        for j in range(CHROMOSOME_SIZE):
            if chromosome[j] is "1":
                weight += int(inventory[j][WEIGHT])
                value += int(inventory[j][VAL])
                volume +=int(inventory[j][VOLUME])

        if weight>MAX_WEIGHT:
            fitness.append(0)
        elif volume > MAX_VOLUME:
            fitness.append(0)
        else:
            fitness.append(value)
        weight = 0
        value = 0
        volume=0
    sum_fitness = sum(fitness)


### GENETIC FUNCTIONS ###
def pick_parent(): #returm index of the parent
    r1 = random.randint(0, 9)
    r2 = random.randint(0, 9)
    r3 = random.randint(0, 9)
    # print(r1,r2,r3)
    vr1 = fitness[r1]
    vr2 = fitness[r2]
    vr3 = fitness[r3]
    return fitness.index(max(vr1, vr2, vr3))


def crossover(index1, index2):
    curr_rate = random.random()

    if curr_rate < CROSSOVER_RATE:
        #i = random.randint(0, CHROMOSOME_SIZE - 1)
        i=int(CHROMOSOME_SIZE/2) #crosing over the half
        l1 = list(chromosomes[index1])
        l2 = list(chromosomes[index2])

        l1 = l2[:i] + l1[i:]
        l2 = l1[:i] + l2[i:]
        return "".join(l1) , "".join(l2)

    return chromosomes[index1], chromosomes[index2]


def mutate(chromosome_list):
    for i in range(GENERATION_SIZE):
        l = list(chromosome_list[i])
        for j in range(CHROMOSOME_SIZE):
            curr_rate = random.random()
            if curr_rate < MUTATION_RATE:
                l[j] = "1" if l[j] is "0" else "0"
                chromosome_list[i] = "".join(l)


def create_new_generation(index):
    global chromosomes
    global fitness

    new_generation = []

    for i in range(int(GENERATION_SIZE / 2)):
        ch1, ch2 = crossover(pick_parent(), pick_parent())
        new_generation.append(ch1)
        new_generation.append(ch2)

    mutate(new_generation)
    chromosomes = new_generation
    fitness = []
    test_fitness()
    if index % int(NUM_GENERATIONS / NUM_TESTS) == 0:
        print("this generation best fit has value of: %d\nthe chromosome is: %s\n" % (max(fitness), chromosomes[fitness.index(max(fitness))]))


### MAIN FUNCTION ###
def main():
    read_file()
    generate_base_generation()
    test_fitness()

    for i in range(NUM_GENERATIONS): #10000
        create_new_generation(i)

main()
