import pandas as pd
from PyInquirer import prompt
import seaborn as sns
import matplotlib.pyplot as plt
from univariate import Univariate
from bivariate import Bivariate


class DataAnalysis:

    describe_choices = [
        "Describe a specific Column",
        "Show Properties of Each Column",
        "Dataframe correlation with heatmap",
        "Show the Dataset",
        "Univariate Analysis",
        "Bivariate Analysis",
        "Go Back",
    ]

    def __init__(self, data, style):
        self.data = data
        self.style = style

    # The function that prints the database on the command line.
    def showDataset(self):
        while 1:
            try:
                rows = int(input(("\nHow many rows(>0) to print?  ")))
                if rows == -1:
                    break
                if rows <= 0:
                    print("Number of rows given must be +ve...\U0001F974")
                    continue
                print(self.data.head(rows))
            except ValueError:
                print("Numeric value is required. Try again....\U0001F974")
                continue
            break
        return

    # function to print all the columns
    def showColumns(self):
        for column in self.data.columns.values:
            print(column, end="  ")

    # function to analyse the dataset or any specific column.
    def describe(self):
        print("\nTasks (Data Description)\U0001F447\n")
        cols = list(self.data.columns)
        columns = []
        for i in cols:
            columns.append({"name": i})

        while 1:
            ques = [
                {
                    "type": "list",
                    "name": "choice",
                    "message": "How would you like to describe the dataset?\n",
                    "choices": self.describe_choices,
                },
            ]
            ans = prompt(ques, style=self.style)
            choice = ans.get("choice")

            if choice == "Go Back":
                break

            elif choice == "Describe a specific Column":
                self.showColumns()
                ques1 = [
                    {
                        "type": "list",
                        "name": "describeColumn",
                        "message": "Which Column?",
                        "choices": columns,
                    },
                ]
                ans1 = prompt(ques1, style=self.style)
                describeColumn = ans1.get("describeColumn")
                print(self.data[describeColumn].describe())

            elif choice == "Show Properties of Each Column":
                # describe() function is used to tell all the info about the database.
                print(self.data.describe())
                print("\n\n")
                print(self.data.info())

            elif choice == "Show the Dataset":
                self.showDataset()

            elif choice == "Dataframe correlation with heatmap":
                sns.heatmap(self.data.corr(), cmap="YlGnBu", annot=True)
                plt.show()

            elif choice == "Univariate Analysis":
                self.data = Univariate(self.data, self.style).univariate()

            elif choice == "Bivariate Analysis":
                self.data = Bivariate(self.data, self.style).bivariate()
