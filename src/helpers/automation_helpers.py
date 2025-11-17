from src.helpers.project_selection_enum import ProjectSelection, SubProblemSelection
import json
from typing import List
from src.helpers.constants import CONFIGURATION_FILE_PATH

def construct_config_json(project_value: ProjectSelection, sub_probs: List[SubProblemSelection]):
    project = {"Selection" : {
        "name" : project_value.name,
        'value' : project_value.value
    }}
    temp = []
    for sub_prob in sub_probs:
        temp.append({"name" : sub_prob.name, "value" : sub_prob.value})
    project["Sub Problem"] =  temp
    config = {"Project Configuration": project}
    with open(CONFIGURATION_FILE_PATH, mode = "w", encoding = "utf-8" ) as conf_buffer:
        json.dump(config, conf_buffer)
    

def brief_about_project():
    print("**********************************************************************************************")
    print("Hello Guys, This is project 1 script for students, This will be asked for the first time,")
    print("once you answer all the questions the program will try to build a configuration file,")
    print("which consists of infroamtion about your project selection.")
    print("based on the configuration setting we will be performing the grading for this project")
    print("NOTE:: Please make sure to answer the questions correctly")
    print("**********************************************************************************************")
    print(" ")
    print(" ")
    print(">>> Here are list of project problems, please select one option among them, NOTE: Input numbers only ")
    print(" ")
    project_dict = {}
    for index,project_name in enumerate(ProjectSelection):
        print(f"{index}. {project_name.value}")
        project_dict[index] = project_name
    project_value = int(input("Please select the number from above::: "))

    print("**********************************************************************************************")
    print(" ")
    print(" ")
    print("Project selected is ",project_dict[project_value].value)
    print(" ")
    print("Please verify it once, if its wrong rerun the program, but terminating it here!!")
    print("**********************************************************************************************")
    print(" ")
    print("A lot of teams have selected mutliple ways to solve, if you are team is working on single solution there")
    print("the entry should be single and followed by alternative option of entering big number which terminates the ")
    print("selection. NOTE: Please follow instructions as stated below")
    print(" ")
    print(">>> Select the methods how want to solve this problem, if you want to terminate this enter any number larger")
    print("the options stated below. this will ask for exact four time")

    sub_problem_array = []

    for index,sub_problem in enumerate(SubProblemSelection):
        print(f" Are you trying to solve the {project_dict[project_value].value} using '{sub_problem.value}'. if yes press 1, else press 0 ")
        sub_problem_value = int(input("Please enter either 1 or 0 ::: "))
        if sub_problem_value > 0:
            sub_problem_array.append(sub_problem)
    
    print(" ")
    print("hurrey now you have build the config, you can actually check them in the configuration folder, feel free to check it out")
    print("")
    print("**********************************************************************************************")
    print(" ")
    print("for reconfirmation here is the options you have selected!!!")
    print(f"Project selected is {project_dict[project_value].value}")
    print(f"You are trying to solve it using below methods")
    for methods in sub_problem_array:
        print(f"*) {methods.value}")
    
    print(" ")
    print("Thank you for the answering the questions now you can start working as per instructions")
    print("********************************************. END  .*********************************************")

    construct_config_json(project_dict[project_value], sub_problem_array)