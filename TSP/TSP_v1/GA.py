from Graph import Graph
import numpy as np
import math

class GA:
    def __init__(self, generations=100, population_size=10, selection_size=4, mutation_rate=0.1, elitismRate=0.1):
        self.generations = generations
        self.population_size = population_size
        self.selection_size = selection_size
        self.mutation_rate = mutation_rate    # in [0,1]
        self.elitismRate = elitismRate  # in [0,1]

    def createPopulation(self, nodes): 
        # avoid duplicates 
        # l = [v for v in np.random.permutation(nodes) for i in range(self.population_size)]   # return a list 
        # print(l)
        # return l
        return [''.join(v for v in np.random.permutation(nodes)) for i in range(self.population_size)]
    
    def evaluateFitness(self, graph, population): 
        return [graph.getCost(path) for path in population]

    def parentSelection(self, graph, population): 
        choices = np.random.choice(population, size = self.selection_size)
        # print(choices)
        fitness = self.evaluateFitness(graph, choices)
        # return choice with minimum distance 
        return choices[np.argmin(fitness)]

    def crossover(self, parent1, parent2):
        children = ['' for i in range(len(parent1))]
        breakpt = np.random.randint(0, len(parent1)-1)
        children[:breakpt+1] = list(parent1)[:breakpt+1]
        indices = list(range(breakpt+1, len(parent1)))        
        for i in parent2:
            if '' not in children:
                break
            if i not in children:
                children[indices.pop(0)] = i
        return ''.join(v for v in children) 

    # mutation via randomly swapping two values --> e.g. 
    def mutation(self, chromosome): 
        if np.random.random() < self.mutation_rate:
            low = np.random.randint(0, len(chromosome)-1)
            high = np.random.randint(low+1, len(chromosome))
            s = list(chromosome)
            s[low], s[high] = s[high], s[low]
            return ''.join(s)
        else:
            return chromosome

    def optimize(self, graph):
        population = self.createPopulation(graph.getVertices())  # list type 
        elitismOffset = math.ceil(self.population_size*self.elitismRate)
        # print ('Optimizing TSP Route for Graph:\n{0}'.format(graph))

        for generation in range(self.generations): # number of generations created 
            print ('\nGeneration: {0}'.format(generation + 1))
            print ('Population: {0}'.format(population))
            
            newPopulation = []       
            fitness = self.evaluateFitness(graph, population)
            print ('Fitness:    {0}'.format(fitness))
            fittest = np.argmin(fitness)

            print ('Fittest Route: {0} ({1})'.format(population[fittest], fitness[fittest]))
            
            if elitismOffset:
                elites = np.array(fitness).argsort()[:elitismOffset]
                [newPopulation.append(population[i]) for i in elites]

            for gen in range(elitismOffset, self.population_size):
                parent1 = self.parentSelection(graph, population)
                parent2 = self.parentSelection(graph, population)
                offspring = self.crossover(parent1, parent2)
                newPopulation.append(offspring)
                # print ('\nParent 1: {0}'.format(parent1))
                # print ('Parent 2: {0}'.format(parent2))
                # print ('Offspring: {0}\n'.format(offspring))
            for gen in range(elitismOffset, self.population_size):
                newPopulation[gen] = self.mutation(newPopulation[gen])
                # print(newPopulation[gen])

            # When all the chromosomes in the next generated population are the same :) 
            if (all(chromosome == newPopulation[0] for chromosome in newPopulation)): 
                print ('\nConverged to a local minima.', end='')
                break
            
            # else continue on
            population = newPopulation

        return (population[fittest], fitness[fittest])


if __name__ == '__main__':
    graph = Graph()
    #f = input("Enter test file name (e.g. test1.txt) : ")
    #file = open(f, "r")
    file = open("test1.txt", "r")
    n = int(file.readline())
    # print(n)
    matrix = file.readlines()
    matrix = [i.split() for i in matrix]
    print(matrix)
    # symmetric matrix 
    for i in range(n):
        for j in range(i+1,n):
            graph.connect(str(i), str(j), matrix[i][j])
    file.close()

    tsp = GA(10, 10, 2, 0.2, 0.1)
    optimal_path, path_cost = tsp.optimize(graph)
    print ('\nPath: {0}, Cost: {1}'.format(optimal_path, path_cost))