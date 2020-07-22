from Graph import Graph
import numpy as np
import math

DEBUG = 1

class GA:
    def __init__(self, generations=100, population_size=10, mutation_rate=0.1, elitismRate=0.1, selection_size=5):
        self.generations = generations
        self.population_size = population_size
        self.mutation_rate = mutation_rate    # in [0,1]
        self.elitismRate = elitismRate  # in [0,1]
        self.selection_size = selection_size

    def createPopulation(self, nodes): 
        # use permutation to avoid duplicates & returns a list 
        return [[v for v in np.random.permutation(nodes)] for i in range(self.population_size)]
    
    def evaluateFitness(self, graph, population): 
        cost = [graph.getCost(path) for path in population]
        fit = [ i/sum(cost)  for i in cost]
        for i in range(1, len(fit)): 
            fit[i] += fit[i-1]
        if DEBUG: 
            print("Cost:    {0}".format(cost))
            print("Fitness: {0}".format(fit))
        return cost, fit

    def parentSelection(self, graph, population): 
        cost, fit = self.evaluateFitness(graph, population)
        parents = []
        for i in range(self.selection_size):
            r = np.random.random() # [0,1]
            for j in range(len(fit)): 
                if r < fit[j]: 
                    index = j
                    break
            parents.append(population[index]) # index is the index of the chosen parent 
        if DEBUG: 
            print("Parents are: {0}".format(parents))

        newcost, newfit = self.evaluateFitness(graph, parents)

        if DEBUG: 
            print("newcost: {0}".format(newcost))
            print(parents[newcost.index(min(newcost))])
        
        # return choice with minimum distance/cost
        return parents[newcost.index(min(newcost))]

    def crossover(self, parent1, parent2):
        children = ['' for i in range(len(parent1))]
        breakpt = np.random.randint(0, len(parent1)-1)
        children[:breakpt+1] = parent1[:breakpt+1]
        indices = list(range(breakpt+1, len(parent1)))        
        for i in parent2:
            if '' not in children:
                break
            if i not in children:
                children[indices.pop(0)] = i
        return [v for v in children]

    # mutation via randomly swapping two values (random index)
    def mutation(self, chromosome): 
        if np.random.random() < self.mutation_rate:
            low = np.random.randint(0, len(chromosome)-1)
            high = np.random.randint(low+1, len(chromosome))
            chromosome[low], chromosome[high] = chromosome[high], chromosome[low]
        return chromosome

    def optimize(self, graph):
        population = self.createPopulation(graph.getVertices())  # list type 
        elitismOffset = math.ceil(self.population_size*self.elitismRate)
        if DEBUG:
            print ('Optimizing TSP Route for Graph:\n{0}'.format(graph))

        for generation in range(self.generations): # number of generations created 
            print ('\nGeneration: {0}'.format(generation + 1))
            print ('Population: {0}'.format(population))
            
            cost, fit = self.evaluateFitness(graph, population)
            print("Cost:     {0}".format(cost))
            print("Fitness:  {0}".format(fit))
            fittest = cost.index(min(cost))
            print ("Fittest Route: {0} (Cost: {1})".format(population[fittest], cost[fittest]))
            
            newPopulation = []   
            # saved elite population from prev generation    
            if elitismOffset:   # non-zero if turned on 
                elites = np.column_stack((np.array(cost), np.array(fit), np.array(population)))
                id = [i for i in range(0,len(elites))]
                elites = np.insert(elites, 0, id, axis=1)
                elites = sorted(elites, key=lambda entry: entry[1])[:elitismOffset]
                for i in elites: 
                    ind = int(i[0][0])
                    newPopulation.append(population[ind])
                if DEBUG:
                    print("newPopulation: {0}".format(newPopulation)) 

            # generate rest of newPopulation
            for gen in range(elitismOffset, self.population_size):
                parent1 = self.parentSelection(graph, population)
                parent2 = self.parentSelection(graph, population)
                offspring = self.crossover(parent1, parent2)
                newPopulation.append(offspring)
                if DEBUG: 
                    print ('\nParent 1: {0}'.format(parent1))
                    print ('Parent 2: {0}'.format(parent2))
                    print ('Offspring: {0}\n'.format(offspring))
            if DEBUG:
                print("newPopulation: {0}".format(newPopulation))

            # avoid mutation on already selected children of elite quality 
            for i in range(elitismOffset, self.population_size):
                newPopulation[i] = self.mutation(newPopulation[i])

            # When all the chromosomes in the next generated population are the same: 
            if (all(chromosome == newPopulation[0] for chromosome in newPopulation)): 
                print("\nThe algorithm converged to a local minima. ")
                break
            # else continue on
            population = newPopulation

        return (population[fittest], cost[fittest])


if __name__ == '__main__':
    graph = Graph()
    file = open("test1.txt", "r")
    n = int(file.readline())
    matrix = file.readlines()
    matrix = [i.split() for i in matrix]
    if DEBUG:
        print(n)
        print(matrix)   # symmetric matrix 
    for i in range(n):
        for j in range(i+1,n):
            graph.connect(str(i), str(j), matrix[i][j])
    file.close()

    # generations=100, population_size=10, mutation_rate=0.1, elitismRate=0.1, selection_size=5
    tsp = GA(50, 10, 0.1, 0.1, 10)
    optimal_path, path_cost = tsp.optimize(graph)
    print ('\nPath (undirected): {0} \nCost (distance)  : {1}'.format(optimal_path, path_cost))