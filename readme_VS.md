# Project 1 Readme Team VS

Version 1 9/11/24  
A single copy of this template should be filled out and submitted with each project submission, regardless of the number of students on the team. It should have the name readme\_”teamname”  
Also change the title of this template to “Project x Readme Team xxx”

| 1 | Team Name: VS |
| :---: | ----- |
| 2 | Team members names and netids: **Vera Casquero (vcasquer) Sofia Cardona (scardon2)** |
| 3 | Overall project attempted, with sub-projects: **SAT: bruteforce and backtracking** |
| 4 | Overall success of the project: **The outputs came back correctly and the plots were representative of the time.** |
| 5 | Approximately total time (in hours) to complete: **Approx. 20** |
| 6 | Link to github repository: [**https://github.com/scardon2/Project1-TOC.git**](https://github.com/scardon2/Project1-TOC.git)  |
| 7 | List of included files (if you have many files of a certain type, such as test files of different sizes, list just the folder): (Add more rows as necessary). Add more rows as necessary.   File/folder Name File Contents and Use Code Files  src/[sat.py](http://sat.py)  results/plot\_generator\_VS.py 1\.  Overall Algorithms for solving SAT problem 2\. Plot generator code to generate timing plots Test Files  input/\*.cnf  In the input folder we have all the test files used for timing and testing accuracy. There are 4 of them. Two used to check and 2 used to check and for timing.  Output Files  results/  There you can find all ouput\_ files that demonstrate the output .csv files that our code generates.  Plots (as needed)  results/  Here you can also find the plots\_ in .png format where you can see the timing plots generated for our timing runs.   |
| 8 | Programming languages used, and associated libraries: **Python (matplotlib, itertools, typing)** |
| 9 | Key data structures (for each sub-project): **Backtracking: dictionaries, and tuples. Brute-force: dictionaries, list of lists File parsing (not a subproject): strings** |
| 10 | General operation of code (for each subproject) **Brute-force: this is a computationally costly algorithm because of how it tries every possible assignment of truth values to the variables. It generates all 2^n combinations, checks each one against all clauses, and returns SAT as soon as it finds an assignment that satisfies the entire CNF. This method is good because it guarantees correctness, but is exponential in time. Backtracking: builds an assignment incrementally, choosing one variable at a time. At each step it assigns true/false, immediately checks for clause conflicts, and backtracks as soon as a partial assignment can’t lead to a solution. This prunes parts of the search space and makes it way faster than brute force, while it also guarantees correctness.** |
| 11 | What test cases you used/added, why you used them, what did they tell you about the correctness of your code. **We used various different SAT problems formatted as explained in a .cnf format. We were able to tell the correctness of the code because our output file matched the whether each problem was Satisfiable or not. Also, for the files that had less examples we were able to check the correctness of our codes proposed T or F assignment by hand.**  |
| 12 | How you managed the code development **First, we worked together to understand the underlying problems to solve and understand the algorithms we had chosen. Then Sofia developed the algorithms, while debugging with a simple sample .cnf. Vera then wrote the test files for the algorithms and made fixes as necessary. Then, wrote the plot generating code and performed timing runs to generate the plots. We then made sure to organize our project and submitted.**  |
| 13 | Detailed discussion of results: **Our results generated an output .csv file that includes whether or not the parsed SAT problem is possible to satisfy or unsatisfiable. How much it takes to solve and the solution if applied. We were able to see how much more efficient the backtracking algorithm is than the bruteforce through our timing runs. We were able to visualize this through the distinct plots.**  |
| 14 | How team was organized **We divided our work as equally as possible. Both focusing on understanding the underlying algorithms while communicating when completing our tasks.**  |
| 15 | What you might do differently if you did the project again **If we were to do the project again, we might have chosen to do another algorithm rather than brute force. Since, naturally for this type of algorithm it was rather simple to code however, its efficiency is terrible and therefore running our timing tests took a very long time.**  |
| 16 | Any additional material: |

   
