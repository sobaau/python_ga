#!/usr/bin/env python3
import random
from datetime import datetime



class Tables:
    last_score = 0

    def __init__(self):
        # random combo from each array.
        self.fitness = 0.0
        self.hints = self.ran_q()

    def get_hints(self):
        return self.hints

    def calc_fitness(self, target):
        pos = 0
        score = 0
        for r in self.hints:
            score += r[2] == 'Toyota Camry' and r[3] == '6am' and r[0] == 'British Couple'
            score += pos == 2 and r[1] == 'Black'
            score += r[2] == 'Hyundai Accent' and r[3] == '9am'
            score += pos > 0 and self.hints[pos - 1][2] == 'Holden Barina' and self.hints[pos - 1][1] == 'Blue' and r[
                0] == 'British Couple'
            score += pos < 4 and r[0] == 'French Lady' and self.hints[pos + 1][4] == 'Gold Coast'
            score += r[2] == 'Nissan X-Trail' and r[4] == 'Sydney'
            score += pos < 4 and r[0] == 'Chinese Businessman' and self.hints[pos + 1][1] == 'Green'
            score += r[4] == 'Newcastle' and r[3] == '5am'
            score += pos < 4 and self.hints[pos + 1][2] == 'Honda Civic' and self.hints[pos + 1][3] == '7am' and r[
                4] == 'Gold Coast'
            score += r[1] == 'Red' and r[4] == 'Tamworth'
            score += pos > 0 and self.hints[pos - 1][1] == 'White' and r[3] == '7am'
            score += pos == 4 and r[0] == 'Indian Man'
            score += r[1] == 'Black' and r[3] == '8am'
            score += pos < 4 and self.hints[pos + 1][0] == 'Indian Man' and r[0] == 'Chinese Businessman'
            score += r[4] == 'Tamworth' and r[3] == '6am'
            pos += 1
        check_dupe = []
        for pop in self.hints:
            for g in pop:
                check_dupe.append(g)
        if not len(set(check_dupe)) == 25:
            score *= 0.9

        self.last_score = score
        self.fitness = (score / target) ** 2

    def crossover(self, partner):
        # new child
        child = Tables()
        midpoint = random.randint(0, len(self.hints) - 1)

        for i in range(len(self.hints)):
            for x in range(len(self.hints)):
                if x > midpoint:
                    child.hints[i][x] = self.hints[i][x]
                else:
                    child.hints[i][x] = partner.hints[i][x]
        return child

    def mutate(self, mut_rate):
        # Based on a mutation probability, picks a new random array combo
        for i in range(len(self.hints)):
            for x in range(len(self.hints)):
                if random.random() < mut_rate:
                    self.hints[i][x] = self.ran_q()[i][x]

        return

    def ran_q(self):
        people = ['British Couple', 'French Lady',
                  'Chinese Businessman', 'Indian Man', 'Canadian Couple']
        colours = ['Green', 'Blue', 'Black', 'Red', 'White']
        car_type = ['Toyota Camry', 'Hyundai Accent',
                    'Nissan X-Trail', 'Honda Civic', 'Holden Barina']
        time = ['5am', '6am', '7am', '8am', '9am']
        destination = ['Newcastle', 'Gold Coast',
                       'Sydney', 'Tamworth', 'Port Macquarie']
        random.shuffle(people)
        random.shuffle(colours)
        random.shuffle(car_type)
        random.shuffle(time)
        random.shuffle(destination)
        attributes = [people, colours, car_type, time, destination]
        total_cars = 5
        rand_answer = []
        for i in range(total_cars):
            rand_answer.append([attr[i] for attr in attributes])
        return rand_answer


class Population:
    m_rate = 0  # Mutation rate
    m_pool = []
    generations = 0
    finished = False
    perfectScore = 1.0

    def __init__(self, t, m, num):
        self.target = t
        self.m_rate = m
        self.population = []
        for i in range(num):
            self.population.append(Tables())

        self.calc_fit()
        self.finished = False
        self.perfectScore = 1.0

    def calc_fit(self):
        for pop in self.population:
            pop.calc_fitness(self.target)
        return

    def natural_selection(self):
        self.m_pool = []
        for i in range(1000):
            max_fit = 0
            fighters = []
            for x in range(40):
                fighter = (random.choice(self.population))
                while fighter in fighters or fighter in self.m_pool:
                    fighter = (random.choice(self.population))
                fighters.append(fighter)
            winner = fighters[1]
            for pop in fighters:
                if pop.fitness > max_fit:
                    max_fit = pop.fitness
                    winner = pop
            self.m_pool.append(winner)

    def generate(self):
        for i in range(len(self.population)):
            a = random.randint(0, len(self.m_pool) - 1)
            b = random.randint(0, len(self.m_pool) - 1)
            while b == a:
                b = random.randint(0, len(self.m_pool) - 1)
            parent_a = self.m_pool[a]
            parent_b = self.m_pool[b]
            child = parent_a.crossover(parent_b)
            child.mutate(self.m_rate)
            self.population[i] = child
        self.generations += 1

    def get_top(self):
        record = 0.0
        index = 0
        for i, pop in enumerate(self.population):
            if pop.fitness > record:
                index = i
                record = pop.fitness
        if record == self.perfectScore:
            self.finished = True
        return self.population[index]

    def get_avg(self):
        total = 0
        for i in self.population:
            total += i.fitness
        return total / len(self.population)


def find_c(answer):
    people = 0
    car = 2
    des = 4
    sol1 = []
    sol2 = []
    for x in range(len(answer)):
        for i in range(len(answer)):
            if answer[x][i] == "Port Macquarie":
                sol1 = answer[i]
            if answer[x][i] == "Canadian Couple":
                sol2 = answer[i]
    print("Answer found!:")
    print("The", sol1[car], "Was going to", sol1[des])
    print("The", sol2[car], "Was hired by the", sol2[people])


def main():
    pop_max = 5000
    mutation_rate = 0.01
    target_answer = 15
    print("This program uses a Genetic Algorithm to attempt to solve a pre-provided Zebra Puzzle")
    print("It has a population of", pop_max, "with a mutation rate of", mutation_rate * 100, "%")
    print("The target is to get 15 of the hints correct from the Zebra Puzzle and hence find the answer to"
          " the question: ")
    print("\tWhich car was going to Port Macquarie? Which car was hired by a Canadian couple?")
    print(
        "This is done by using constraints from the hints and using True or False (1 and 0) to")
    print("calculate the total right hints and then fitness of that table on a scale of 0 to 1.")
    print(
        "To avoid duplicates in the answer the AI is punished within the fitness function if any duplicates are found.\n")
    print("Mating pool selection is performed with a Tournament Selection of 1000 rounds and 40 fighters,")
    print("The 40 fighters selected can not be in the current mating pool and will be reselected if they are.")
    print("The single strongest of these fighters are then added to the mating pool which will have a total size of 1000")
    print("After this the Parents are picked at random from the mating pool, These parents can not be the same parent.")
    print("The Child is created from these Parents by selecting random parts of their tables to crossover and then once")
    print("this is finished the child is mutated in random locations depending on the mutation rate provided.\n")
    print(
        "To avoid any Premature Convergence and hence stalling of the Algorithm it is restarted after "
        "100 iterations.\n")
    print("By David Preston - 220156331\n")
    input("Press Enter to continue")
    start_time = datetime.now()
    iterations = 0
    total_gen = 0
    pop = Population(target_answer, mutation_rate, pop_max)
    while not pop.finished:
        if pop.generations % 100 == 0:
            iterations += 1
            total_gen += pop.generations
            pop = Population(target_answer, mutation_rate, pop_max)
        pop.natural_selection()
        pop.generate()
        pop.calc_fit()
        total_gen += pop.generations
        print("Iteration #", iterations)
        print("Generation #", pop.generations)
        print("Mutation Rate:", pop.m_rate * 100, "%")
        print("Average Fitness:", round(pop.get_avg() * 100, 3), "%")
        print("Best Fitness score:", round(pop.get_top().fitness * 100, 3), "%")
        print("Total hints from this score:", pop.get_top().last_score)
        print("Best Guess:")
        i = 1
        for car in pop.get_top().get_hints():
            print("Spot #", i, car)
            i += 1
        print("--------------------------------------------------------------------------")

    find_c(pop.get_top().get_hints())
    print('It took a total number of', iterations, "iterations and total of", iterations * pop.generations,
          "generations to find our answer with a total run time of",
          datetime.now() - start_time)


if __name__ == "__main__":
    main()
