import pandas as pd
from PyInquirer import prompt
import matplotlib.pyplot as plt


class Univariate:
    def __init__(self, data, style):
        self.data = data
        self.style = style

    # main function of the Univaraite Class.
    def univariate(self):
        cols = list(self.data.select_dtypes(exclude="object"))
        columns = []
        for i in cols:
            columns.append({"name": i})

        print("\nUnivariate Analysis\U0001F447")

        while 1:
            ques = [
                {
                    "type": "list",
                    "name": "col",
                    "message": "Select column for analysis",
                    "choices": columns,
                }
            ]
            ans = prompt(ques, style=self.style)
            col = ans.get("col")
            ques1 = [
                {
                    "type": "list",
                    "name": "var",
                    "message": "What do you want?",
                    "choices": [
                        "Histogram",
                        "LinePlot",
                        "BoxPlot",
                        "Go Back",
                    ],
                }
            ]
            ans1 = prompt(ques1, style=self.style)
            choice = ans1.get("var")

            if choice == "Go Back":
                break

            elif choice == "Histogram":
                self.data[col].plot.hist()
                plt.ylabel(col)
                plt.show()

            elif choice == "LinePlot":
                self.data[col].value_counts().sort_index().plot.line()
                plt.ylabel(col)
                plt.show()

            elif choice == "BoxPlot":
                self.data[col].plot.box()
                plt.ylabel(col)
                plt.show()

            elif choice == "Show the Dataset":
                DataDescription.showDataset(self)

        # Returns all the changes on the DataFrame.
        return self.data
