from Classes import Population, Chromosome, Grid, Crossover
import numpy as np
import random

class Sudoku():
    def __init__(self):
        self.game = None

    def GA(self, path, populationSize=200, elitismRate=0.6, generationNo=1500, mutationRate=0.2, selectionRate=0.85, resetNo=100):
        with open(path, "r") as f:
            values = np.loadtxt(f).astype(int)
            self.game = Grid(values)
        print("Initial Game: \n", values)
        eliteSize = int(populationSize * elitismRate)
        repeatedNo = 0
        prevFit = 0

        # Generate initial population: 
        self.population = Population()
        self.population.createPopulation(populationSize, self.game)

        for gen in range(generationNo):
            print("\nGeneration:  %d" % gen)
            bestFit = 0
            bestSol = self.game
            for c in range(populationSize):
                fitness = self.population.chromosomes[c].fitness
                value = self.population.chromosomes[c].values
                # Solution can only be found with perfect fitness (value of 1)
                if int(fitness) == 1:
                    print("Solution Found! ")
                    print(value)
                    print("Fitness Value: 1.0 ")
                    return
                if fitness > bestFit:
                    bestFit = fitness
                    bestSol = value
            print(self.population.chromosomes[c].values)
            print("Fitness Value: %f" % bestFit)

            # Generate the next population with elite values to keep
            nextPopulation = []
            self.population.sort()
            elites = []
            for e in range(eliteSize):
                elite = Chromosome()
                elite.values = np.copy(self.population.chromosomes[e].values)
                elites.append(elite)

            # Generate the rest of the chromosomes
            for i in range(eliteSize, populationSize):
                t = Crossover()
                parent1 = t.chooseParent(self.population.chromosomes, selectionRate)
                parent2 = t.chooseParent(self.population.chromosomes, selectionRate)
                child1, child2 = t.crossover(parent1, parent2)

                # Mutate child1 & child2.
                child1.mutate(mutationRate, self.game)
                child1.updateFitness()
                child2.mutate(mutationRate, self.game)
                child2.updateFitness()
                # Add children to new population.
                nextPopulation.append(child1)
                nextPopulation.append(child2)

            # Append elites to the population. 
            # These will not have been affected by crossover or mutation.
            for e in range(eliteSize):
                nextPopulation.append(elites[e])
                
            # Select next generation.
            self.population.chromosomes = nextPopulation
            self.population.updateFitness()
            self.population.sort()

            if gen == 0:
                prevFit = bestFit
                repeatedNo = 1
            if prevFit == bestFit:
                repeatedNo += 1
            else:
                repeatedNo = 0
                prevFit = bestFit


            # Reset the whole population if the number of repeating generations with the same fitness
            # has exceeded the resetNo
            if repeatedNo >= resetNo:
                print("Algorithm is NOT converging! Reseeding the Population.")
                self.population.createPopulation(populationSize, self.game)
                repeatedNo = 0
                mutations = 0

        print("Algorithm did not converge. No solution found. :( ")
        print("Best Solution So Far: \n", bestSol)

if __name__ == "__main__":
    f = input("Enter input file name: ")
    Sudoku().GA(f)