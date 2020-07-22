# Sudoku Solver Project

The project implements a Sudoku game solver using genetic algorithm. 

## Running Instructions:

The user can simply run the following command to start the program:
$ python3 Sudoku.py

Then the program prompts the user to enter the input file name:
Enter input file name: 

Example input files are included in the folder: easy.txt, hard.txt

## Example Input:

0 0 4 0 8 0 3 0 0
0 0 0 0 0 3 0 4 2
8 0 0 4 0 5 9 0 7
3 0 2 0 7 0 5 0 8
0 5 0 0 0 0 0 7 0
6 0 8 0 9 0 2 0 1
4 0 6 2 0 7 0 0 9
5 2 0 9 0 0 0 0 0
0 0 7 0 1 0 4 0 0

## Fitness Evaluation Method

The fitness value is 1 if all the blocks are filled in the 9 by 9 grid.
Otherwise, the fitness value is calculated based on the sum of values filled 
on each row, column and 3 by 3 grid. 

The higher the fitness value, the closer is the grid to the solution. 

## Mutation Method

Mutation is conducted via randomly picking a row to mutate, and then randomly 
pick two columns within that row to swap values. 

## Crossover Method

Cycle Crossover is used. More detailed description can be found here:
http://www.rubicite.com/Tutorials/GeneticAlgorithms/CrossoverOperators/CycleCrossoverOperator.aspx


## Author

* **Cecilia Y. Sui** - Artificial Intelligence Course (Spring 2020)