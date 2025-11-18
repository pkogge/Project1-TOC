| # | Item                  | Details            |
| - | --------------------- | ------------------ |
| 1 | Team Name             | Problem Solverz    |
| 2 | Team Members & NetIDs | AJ Jones, ajones42 |
| # | Item                       | Details                                                         |
| - | -------------------------- | --------------------------------------------------------------- |
| 3 | Overall Project Attempted  | Backtracking SAT Solver – DPLL Implementation                   |
| 4 | Overall Success            | Pretty successful; test files pass and works on larger datasets |
| 5 | Approx. Total Time (hours) | 6–7                                                             |
| 6 | GitHub Repository          | [Link](https://github.com/ajones2005/Project1-TOC.git)          |
| File/Folder                           | Contents & Use                                                           |
| ------------------------------------- | ------------------------------------------------------------------------ |
| `sat_solver.py`                       | Main algorithm implementation, file input/output, unit propagation       |
| `2SAT.cnf`, `cnffile.cnf`, `kSAT.cnf` | Test files in DIMACS CNF format; test solver on small and large datasets |
| `resultsfile.csv`                     | Output file with instance ID, variables, clauses, and method used        |
| # | Item                  | Details                    |
| - | --------------------- | -------------------------- |
| 8 | Languages & Libraries | Python, os, sys, csv, time |
| # | Item            | Details                                                                                                                                                          |
| - | --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 9 | Data Structures | List of lists (CNF formula), dict (variable assignments), dict (polarity for pure literals), tuple (CNF representation), dict (solution output), list (CSV rows) |
| #  | Item           | Details                                                                                                                                                                                                                                                                                                         |
| -- | -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 10 | Code Operation | The SAT solver solves boolean formulas in CNF using a backtracking DPLL algorithm. Input CSV files contain CNF formulas. The solver uses recursive backtracking enhanced by unit propagation and pure literal elimination. Early termination occurs when all clauses are satisfied or a contradiction is found. |
| #  | Item       | Details                                                                                                                                                                                      |
| -- | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 11 | Test Cases | CNF formulas with various variables and clauses. Tautologies test simplification, repeated clauses test robustness, multiple instances per file test solver’s ability to separate instances. |
| #  | Item                 | Details                                                                                                     |
| -- | -------------------- | ----------------------------------------------------------------------------------------------------------- |
| 12 | Development Approach | Conducted research on DPLL, watched tutorials, divided problem into sub-problems, and tested incrementally. |
| #  | Item               | Details                                                                                                                                                                                                                                                                                                                                                                                                                       |
| -- | ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 13 | Results Discussion | Tested on three CNF instances with 4 variables and 10 clauses each. Problem 1 was unsatisfiable; Problems 2 and 3 were satisfiable with assignments `{1: True, 2: True, 3: True, 4: False}` and `{1: False, 2: False, 3: True, 4: True}`. Low computation times indicate efficiency with unit propagation, pure literal elimination, and backtracking. The solver reliably identifies satisfiable and unsatisfiable formulas. |
| #  | Item              | Details               |
| -- | ----------------- | --------------------- |
| 14 | Team Organization | Single member project |
| #  | Item                           | Details                                                                                                                                                                   |
| -- | ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 15 | What Would Be Done Differently | Incorporate more automated testing, including edge cases with large formulas, redundant clauses, and known UNSAT instances to verify correctness and measure performance. |
| #  | Item      | Details                                                                                                                              |
| -- | --------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| 16 | Resources | [YouTube Video](https://www.youtube.com/watch?v=opppqIdiX-A&t=5294s), [DPLL Wikipedia](https://en.wikipedia.org/wiki/DPLL_algorithm) |
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Overview: These instructions provide you with a skeleton python definition for each problem type. After cloning this repo, you will modify only those functions that you have signed up for (at most 3 for a three person group)
* You will clone a repo that has skeleton code for each possible program.
* You will modify the body of your selected code for your implementation. Do not change the arguments.
* Your output should be a csv file - format given in the python comments for each function.
* Instructions are also included on running your code when you want to test it.
* When you modified code is called the arguments to the function on each call provide a test case (you do not need to read test cases rom any files with this procedure).
* The testing infrastructure will feed the test problems to your code one at a time, will accumulate your responses to it, and will return a score.
* The "input" folder holds the test cases that the above mechanism will use when you run your tests.
* The test cases to be used for grading are separate, and are not visible to you.
* If you need to access other python packages in your code, the UV package discussed below can give your functions access to them.
* Send all questions about this infrastructure to Laxminarayana Vadnala lvadnala@nd.edu

<!-- ## instructions to generate a PAT (a Personal Access Token): -->


<!-- * Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
* Click "Generate new token" → "Generate new token (classic)"
* Set expiration (90 days recommended)
* Select scopes: repo (full control of private repositories)
* Generate token and copy it -->


## Student Instructions to clone the repository and how to run and finally submit the assignment:
------------------
* From your browser, go to [GITHUB URL](https://github.com/pkogge/Project1-TOC) and click the fork button as shown in the picture below


![fork_button](documentation/assets/fork_button.png "fork button")


* You will now enter the fork screen, from here make sure to select your own github account which is highlighted in screen below (for instance, I have selected my own personal account), after that click on the `create fork` button highlighted in orange arrow and box.

![fork_screen](documentation/assets/fork_screen.png "fork screen")

* You will now see the screen which looks like below, the first red box on left should reflect your own github account and should say forked from `forked from pkogge/Project1-TOC.` Then you can follow general instructions of cloning the github repository. Here is the [Docs Link](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) that can help you to clone the github repository on your computer.

![cloned_repo](documentation/assets/cloned_repo.png "cloned_repo")

* Once you clone the repository, open the project in the IDE of your choice.

### Getting started with the python support package manager "UV" installation.
----------------

* Start  by installing `UV` in your machine. Here is the [instructions page](https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_1) that helps you to install the `UV`.

* Immediately after installing it run command `uv sync` which installs the pytests and other required packages.

* NOTE: If you are struggling with installing `UV` please feel to reach me out via slack, I can help you navigate. lvadnala@nd.edu

* This project template is equipped with all the packages required for your project. No additional python packages are required to be installed, but if you want to install additional python packages make sure use the command `uv add <python-package-name>` (mostly it is not useful).

### How can we run the code using UV when other packages are needed
----------------
* For this project I am using UV to demonstrate to run the code. Basically you need to use the command `uv run main.py` from the root of the project folder in the terminal to see your code executes.
* Immediately after cloning the repository, and you didnt do any code changes, if you run the command `uv run main.py` you would see the results below.

```
lax@Mac Project1-TOC % uv run main.py
Hello from project1_toc!
```

* the `Hello from project1_toc` message states that you are good to make changes to the code.

### Making changes to the code and running the test cases of your own
----------------

* Here is the folder structure that every student should make changes to. This is personalized for SAT, but the others are similar. The src directory hold the code you want to modify.

```
.
|── src/
│   |── entrypoint.py
|-- results/
|   |-- SATu.cnf
|-- module_tests/
|   |-- test_sample.py
|-- main.py
```

* The `src/entrypoint.py` file contains the function called as `main.` Make sure to add all your auxikiary files into the `src` folder and make sure to use the `entrypoint.py` file's main function as your main function Dont change this structure as if you do the automation wont be able to perform the grading.
* The `results` folder is where you should save your results from the project. For SAT the project is expected to generate `cnf` files which are basically the CSV files, make sure to save all the results generated by code to results folder (!!! This is most important otherwise you might loose points).
* The `module_tests` is the folder where you can add your own custom test cases. If you are familiar with pytests you can do so, but it is not compulsory to add test cases to the project, its totally the students choice to add, since the pytests have a little learning curve.
* `main.py` please dont edit this file, this is the main file and it should stay like this.
* Once you add your own test cases please make sure to run the `uv run pytest -s` (optional step, should only perform this if you haev added test cases as per the pytest standard)


### Commit the code and make sure to raise a PR (Pull Request)
---------------

* Push the changes to the repositiory. Here is the [Docs Link](https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository) that helps you with basic git commands to push the code.
* Now the last step is to raise the PR to the Forked repo, here is the [Docs link](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork)
* Please update the PR link to the [Teams Spread Sheet](https://docs.google.com/spreadsheets/d/1FYyJMDnft__n0SohcIcSL7lUO60RMtJk9nuVJ5l30SY/edit?usp=sharing) shared by Dr. Kogge. This is most important since we grade only the links that are part of the teams spreadsheet.
