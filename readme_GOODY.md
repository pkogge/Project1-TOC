# Project Teamwork Template

**Version 1 9/11/24**

A separate copy of this template should be filled out and submitted by each student, regardless of the number of students on the team. Also change the title of this template to "Project x Teamwork <GOODY> - <egoodrow>"

---

1. **Team Name:** GOODY

2. **Individual name:** Eve Goodrow

3. **Individual netid:** egoodrow

4. **Other team members names and netids:**

5. **Link to github repository:**

6. **Overall project attempted, with sub-projects:** SAT Solving, brute force

7. **List of Included files (if you have many files of a certain type, such as test files of different sizes, list just the folder): (Add more rows as necessary)**

---

## File/Folder Contents

| File/folder Name | File Contents and Use |
|------------------|----------------------|
| **Code Files** | |
| Main.py | Contains entrypoint call |
| student_config.json | Contains information about project and title |
| sat.py | Contains bruteforce function that demonstrates time complexity of solving a SAT problem by testing every single possible variable assignment until you find one that works |
| entrypoint.py | Saves directions for different projects – I am doing SAT solving so points to that instead of graphnoiso or other choices of problem |
| sat_solver_helper.py | Helps write and format my output to make it work for a csv file |
| constants.py | Keeps constants such as my input file name and other variables that are unchanged throughout my runtime |
| **Test Files** | |

2SAT.cnf	Used the given test files downloaded from canvas. Has many instances of different clauses with different variable lengths. The least is 4 variables and the most is 28
kSAT.cnf	Used the given test files downloaded from canvas. Has many instances of different clauses with different variable lengths. The least is 4 variables and the most is 24
cnffile.cnf	Used the given test files downloaded from canvas. Has many instances of different clauses with different variable lengths. The least is 4 variables and the most is 22
Output Files
brute_force_2SAT_sat_solver_results.csv
	Gives the output of every instance in my 2SAT test file. Includes the columns: instance, n_vars (how many variables there were), n_clauses (how many clauses there were), method (all were brute force), satisfiability, time in seconds, and solution (if applicable). This output was then transferred to a csv file allowing me to graph the output
brute_force_cnffile_sat_solver_results.csv
	Gives the output of every instance in my cnffile test file. Includes the columns: instance, n_vars (how many variables there were), n_clauses (how many clauses there were), method (all were brute force), satisfiability, time in seconds, and solution (if applicable). This output was then transferred to a csv file allowing me to graph the output
brute_force_kSAT_sat_solver_results.csv	Gives the output of every instance in my kSAT test file. Includes the columns: instance, n_vars (how many variables there were), n_clauses (how many clauses there were), method (all were brute force), satisfiability, time in seconds, and solution (if applicable). This output was then transferred to a csv file allowing me to graph the output
Plots (as needed)
2SAT.xlsx	 
Shows exponential growth correlated to number of variables
kSAT.xlsx	 
Shows exponential growth correlated to number of variables
cnffile.xlsx	 

Shows exponential growth correlated to number of variables

Individual Student time (in hours) to complete: 10 hours
Your specific activities and responsibilities: everything
-	Designing logistics
-	Coding the brute force algorithm
-	Transferring and plotting the data
-	Analyzing the graphs
What was personally learned (topic, programming, algorithms)
-	I learned how inefficient brute force algorithms are. It took me an extremely long time to run all the datasets that were given and it was frustrating to not be able to do anything about it. I also learned that simply adding one for loop will change my runtime drastically. I always knew that but this problem showed it in action. I learned how to code different algorithms, and especially how to work excel graphs, which was honestly the biggest learning curve. I also learned the importance of formatting in cnf files. Originally, one of the cnf files I tried to download had mismatch format which completely threw my algorithm off. Finally, I improved my Github and organizational skills with the use of many different platforms to ultimately turn in the final product. 
-	Clearly, as the number of variables increase, the runtime grows exponentially
How team was organized, and what might be improved.
-	In the future, it would have been nice to have someone to bounce ideas off of. I might try working with someone next time.
Any additional material:

-	It was really difficult for me to keep track of everything I needed because we are using so many different platforms and we did not have much guidance or experience with using github like this
<img width="468" height="635" alt="image" src="https://github.com/user-attachments/assets/b8b511eb-68e8-4910-b4c4-c4fd7b1622f3" />


