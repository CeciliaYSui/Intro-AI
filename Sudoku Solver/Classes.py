import numpy as np
import random

class Grid():
    def __init__(self, values):
        self.values = values

    def gridDup(self, row, col, value):
        r, c = 3*(int(row/3)), 3*(int(col/3))
        return True if ((self.values[r][c] == value)
           or (self.values[r][c+1] == value)
           or (self.values[r+1][c] == value)
           or (self.values[r][c+2] == value)
           or (self.values[r+2][c] == value)
           or (self.values[r+1][c+2] == value)
           or (self.values[r+2][c+1] == value)
           or (self.values[r+1][c+1] == value)
           or (self.values[r+2][c+2] == value)) else False

    def rowDup(self, row, value):
        for col in range(9):
            if self.values[row][col] == value:
               return True
        return False

    def colDup(self, col, value):
        for row in range(9):
            if self.values[row][col] == value:
               return True
        return False

class Population():
    def __init__(self):
        self.chromosomes = []

    def createPopulation(self, populationSize, grid):
        self.chromosomes = []
        possible = Chromosome()
        possible.values = [[[] for i in range(9)] for j in range(9)]
        for row in range(9):
            for col in range(9):
                for value in range(1, 10):
                    tmp = grid.values[row][col]
                    if tmp != 0:
                        possible.values[row][col].append(tmp)
                        break
                    # if no duplicated values & the block has not been filled
                    if ((tmp == 0) and not (grid.rowDup(row, value) or grid.colDup(col, value) or grid.gridDup(row, col, value))):
                        possible.values[row][col].append(value)
        for p in range(populationSize):
            g = Chromosome()
            for i in range(9):
                row = np.zeros(9, dtype=int)
                for j in range(9):
                    tmp = grid.values[i][j]
                    row[j] = possible.values[i][j][random.randint(0, len(possible.values[i][j])-1)] if (tmp==0) else tmp
                while (len(list(set(row))) != 9):
                    for j in range(9):
                        if (grid.values[i][j] == 0):
                            row[j] = possible.values[i][j][random.randint(0, len(possible.values[i][j])-1)]
                g.values[i] = row
            self.chromosomes.append(g)
        self.updateFitness()
        
    def updateFitness(self):
        [c.updateFitness() for c in self.chromosomes]
  
    def sort(self):
        # sorting based on fitness values 
        for i in range(len(self.chromosomes)-1):
            MAX = i
            for j in range(i+1, len(self.chromosomes)):
                if self.chromosomes[MAX].fitness < self.chromosomes[j].fitness:
                    MAX = j
            self.chromosomes[i], self.chromosomes[MAX] = self.chromosomes[MAX], self.chromosomes[i]

class Chromosome():
    def __init__(self):
        self.values = np.zeros((9, 9), dtype=int)
        self.fitness = None

    def updateFitness(self):
        colCnt, blockCnt, rowCnt = np.zeros(9, dtype=int), np.zeros(9, dtype=int), np.zeros(9, dtype=int)
        colSum, blockSum, rowSum = 0, 0, 0
        # For each row: 
        for i in range(9):
            filled = 0 # already filled values
            for j in range(9):
                rowCnt[self.values[i][j]-1] += 1
            for k in range(9):
                filled += 1 if (rowCnt[k] != 0) else 0
            rowSum += (filled/9)
            rowCnt = np.zeros(9, dtype=int) # reset 

        # For each column: 
        for i in range(9):
            filled = 0 # already filled values
            for j in range(9):  
                colCnt[self.values[j][i]-1] += 1
            for k in range(9):
                filled += 1 if (colCnt[k] != 0) else 0
            colSum += (filled/9)
            colCnt = np.zeros(9, dtype=int) # reset 

        # For each block of 3 X 3: 
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                blockCnt[self.values[i][j]-1] += 1
                blockCnt[self.values[i][j+1]-1] += 1
                blockCnt[self.values[i][j+2]-1] += 1
                blockCnt[self.values[i+1][j]-1] += 1
                blockCnt[self.values[i+1][j+1]-1] += 1
                blockCnt[self.values[i+1][j+2]-1] += 1
                blockCnt[self.values[i+2][j]-1] += 1
                blockCnt[self.values[i+2][j+1]-1] += 1
                blockCnt[self.values[i+2][j+2]-1] += 1
                filled = 0
                for k in range(9):
                    filled += 1 if (blockCnt[k] != 0) else 0
                blockSum += (filled/9)
                blockCnt = np.zeros(9, dtype=int) 
        fitness = 1 if (int(rowSum)==9 and int(colSum)==9 and int(blockSum)==9) else (rowSum*colSum*blockSum/729)
        self.fitness = fitness
        
    def mutate(self, mutationRate, grid):
        flag = True
        if random.random() < mutationRate:
            while flag:
                row = random.randint(0, 8)
                col1 = random.randint(0, 8)
                col2 = random.randint(0, 8)
                while col2 == col1:
                    col2 = random.randint(0, 8)   
                if grid.values[row][col1] == 0 and grid.values[row][col2] == 0 and not (grid.colDup(col1, self.values[row][col2]) 
                    or grid.colDup(col2, self.values[row][col1]) or grid.gridDup(row, col1, self.values[row][col2])
                    or grid.gridDup(row, col2, self.values[row][col1])):
                    # Mutate! swap values.
                    self.values[row][col1], self.values[row][col2] = self.values[row][col2], self.values[row][col1]
                    flag = False

class Crossover():
    # Cycle Crossover is used here. Details can be found here:
    # http://www.rubicite.com/Tutorials/GeneticAlgorithms/CrossoverOperators/CycleCrossoverOperator.aspx
    def chooseParent(self, chromosomes, selectionRate):
        c1 = chromosomes[random.randint(0, len(chromosomes)-1)]
        c2 = chromosomes[random.randint(0, len(chromosomes)-1)]
        if c1.fitness < c2.fitness:
            c1, c2 = c2, c1
        return c1 if (random.random() < selectionRate) else c2
    
    def crossover(self, parent1, parent2):
        child1, child2 = Chromosome(), Chromosome()
        child1.values = np.copy(parent1.values)
        child1.fitness = parent1.fitness
        child2.values = np.copy(parent2.values)
        child2.fitness = parent2.fitness
        # Crossover needs at least 1 row
        breakpt1 = random.randint(0, 8)
        breakpt2 = random.randint(1, 9)
        while breakpt2 == breakpt1:
            breakpt2 = random.randint(1, 9)    
        if breakpt1 > breakpt2:
            breakpt1, breakpt2 = breakpt2, breakpt1
        for i in range (breakpt1, breakpt2):
            tmp1, tmp2 = np.zeros(9), np.zeros(9)
            row1, row2 = child1.values[i], child2.values[i]
            remaining = [j for j in range(1, 10)]
            cycle, index = 0, 0
            # child rows not complete
            while (0 in tmp1) and (0 in tmp2):
                for j in range(len(row1)):
                    if row1[j] in remaining:
                        index = j
                start = row1[index]
                remaining.remove(row1[index])
                value = row2[index]
                # Even Cycles
                if cycle % 2 == 0:
                    tmp1[index], tmp2[index] = row1[index], row2[index]
                    while value != start: 
                        for j in range(len(row1)):
                            if (row1[j] == value):
                                index = j
                        tmp1[index], tmp2[index] = row1[index], row2[index]
                        value = row2[index]
                        remaining.remove(row1[index])
                # Odd Cycles
                else: 
                    tmp1[index], tmp2[index] = row2[index], row1[index]
                    while (value != start):
                        for j in range(len(row1)):
                            if (row1[j] == value):
                                index = j
                        tmp1[index], tmp2[index] = row2[index], row1[index]
                        value = row2[index]
                        remaining.remove(row1[index])
                cycle += 1
            child1.values[i], child2.values[i] = tmp1, tmp2
        return child1, child2