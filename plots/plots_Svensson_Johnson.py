import matplotlib.pyplot as plt
import csv
import os


for root, dirs, files in os.walk(results_dir):
    for filename in files:
        full_path = os.path.join(root, filename)
        if "brute_force" in filename:
            with open(full_path) as csvfile:
                csvlist = list(csv.reader(csvfile))

            xVals = [] # number of instances
            yVals = [] # timing
            color = [] # colors

            for index, item in enumerate(csvlist):
                if index == 0: continue
                xVals.append(int(item[1]))
                yVals.append(float(item[5]))
                if item[4] == 'U': color.append('red')
                if item[4] == 'S': color.append('green')

            plt.scatter(xVals, yVals, c=color)
            plt.xlabel("Number of Instances")
            plt.ylabel("Time (s)")
            plt.title("Brute Force")
            plt.show()

        if "btracking" in filename:
            with open(full_path) as csvfile:
                csvlist = list(csv.reader(csvfile))
            xVals = [] # number of instances
            yVals = [] # timing
            color = [] # colors

            for index, item in enumerate(csvlist):
                if index == 0: continue
                xVals.append(int(item[1]))
                yVals.append(float(item[5]))
                if item[4] == 'U': color.append('red')
                if item[4] == 'S': color.append('green')

            plt.scatter(xVals, yVals, c=color)
            plt.xlabel("Number of Instances")
            plt.ylabel("Time (s)")
            plt.title("Backtracking")
            plt.show()

