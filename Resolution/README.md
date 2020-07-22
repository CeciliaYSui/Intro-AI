# Project 3: Resolution

Course ----------- Artificial Intelligence <br>
Author ----------- Cecilia Y. Sui <br>
Submission Date -- March 1, 2020 <br>
Language Used ---- Python 3.7.1 <br>

# How to execute: 

Run the following command in terminal: <br>
$ python3 project3.py

# Input Format: 

The input is the set of clauses in the CNF representation of KB ∧ ¬α . <br>
Since it is in CNF, the only operators that will be present in the input are: "v" and "¬". <br>

Example input: <br>
A v B<br>
¬ B v C<br>
¬ A v C<br>
¬ C<br>

There are multiple example input files provided in the folder submitted.

# Output:

return True if a contradiction is resolved (i.e. KB entails alpha) <br>
return False otherwise