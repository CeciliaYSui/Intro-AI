from Graph import Graph
import numpy as np
import math

DEBUG = 0

class GA:
    def __init__(self, generations=100, sizeP=10, mutationR=0.1, bestOnes=0.1, sizeN=5):
        self.generations = generations
        self.sizeP = sizeP
        self.mutationR = mutationR    # in [0,1]
        self.bestOnes = bestOnes  # in [0,1]
        self.sizeN = sizeN

    def createPopulation(self, nodes): 
        return [[v for v in np.random.permutation(nodes)] for i in range(self.sizeP)]
    
    def evaluateFitness(self, graph, population): 
        cost = [graph.getCost(path) for path in population]
        fit = [ i/sum(cost)  for i in cost]
        for i in range(1, len(fit)): 
            fit[i] += fit[i-1]
        if DEBUG: 
            print("Cost:    {0}".format(cost))
            print("Fitness: {0}".format(fit))
        return cost, fit

    def chooseParent(self, graph, population): 
        cost, fit = self.evaluateFitness(graph, population)
        parents = []
        for i in range(self.sizeN):
            r = np.random.random() # [0,1]
            for j in range(len(fit)): 
                if r < fit[j]: 
                    index = j
                    break
            parents.append(population[index])
        newcost, newfit = self.evaluateFitness(graph, parents)
        if DEBUG: 
            print("Parents are: {0}".format(parents))
            print("newcost: {0}".format(newcost))
            print(parents[newcost.index(min(newcost))])        
        return parents[newcost.index(min(newcost))]

    def crossover(self, parent1, parent2):
        children = [None for i in range(len(parent1))]
        breakpt = np.random.randint(0, len(parent1)-1)
        children[:breakpt+1] = parent1[:breakpt+1]
        indices = list(range(breakpt+1, len(parent1)))        
        for i in parent2:
            if None not in children:
                break
            if i not in children:
                children[indices.pop(0)] = i
        return [v for v in children]

    def mutation(self, chromosome): 
        if np.random.random() < self.mutationR:
            low = np.random.randint(0, len(chromosome)-1)
            high = np.random.randint(low+1, len(chromosome))
            chromosome[low], chromosome[high] = chromosome[high], chromosome[low]
        return chromosome

    def TSP(self, graph):
        population = self.createPopulation(graph.getVertices())
        offset = math.ceil(self.sizeP * self.bestOnes)
        if DEBUG:
            print ("TSP Graph:\n{0}".format(graph))

        for generation in range(self.generations): 
            print ("\nGeneration: {0}".format(generation))
            if DEBUG:
                print ("Population: {0}".format(population))
            
            cost, fit = self.evaluateFitness(graph, population)
            fittest = cost.index(min(cost))
            if DEBUG:
                print("Cost:     {0}".format(cost))
                print("Fitness:  {0}".format(fit))
            print("Fittest Route: {0} (Cost: {1})".format(population[fittest], cost[fittest]))
            
            newPopulation = []   
            # saved elite population from prev generation    
            if offset:   # non-zero if turned on 
                preserved = np.column_stack((np.array(cost), np.array(fit), np.array(population)))
                id = [i for i in range(0,len(preserved))]
                preserved = np.insert(preserved, 0, id, axis=1)
                preserved = sorted(preserved, key=lambda entry: entry[1])[:offset]
                for i in preserved: 
                    ind = int(i[0][0])
                    newPopulation.append(population[ind])
                if DEBUG:
                    print("newPopulation: {0}".format(newPopulation)) 

            # generate rest of newPopulation
            for gen in range(offset, self.sizeP):
                parent1 = self.chooseParent(graph, population)
                parent2 = self.chooseParent(graph, population)
                offspring = self.crossover(parent1, parent2)
                newPopulation.append(offspring)
                if DEBUG: 
                    print ("Parent 1: {0}".format(parent1))
                    print ("Parent 2: {0}".format(parent2))
                    print ("Offspring: {0}".format(offspring))
            if DEBUG:
                print("newPopulation: {0}".format(newPopulation))

            for i in range(offset, self.sizeP):
                newPopulation[i] = self.mutation(newPopulation[i])

            # When all the chromosomes in the next generated population are the same: 
            if (all(chromosome == newPopulation[0] for chromosome in newPopulation)): 
                print("\nThe algorithm converged to a local minimum. ")
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

    # default: generations=100, population_size=10, mutation_rate=0.1, elitismRate=0.1, selection_size=5
    result = GA(10, 10, 0.1, 0.1, 5)
    path, cost = result.TSP(graph)
    print ("\nPath (undirected): {0} \nCost (distance)  : {1}".format(path, cost))