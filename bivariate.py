import pandas as pd
from PyInquirer import prompt
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm


class Bivariate:
    def __init__(self, data, style):
        self.data = data
        self.style = style

    # main function of the Univaraite Class.
    def bivariate(self):
        cols = list(self.data.select_dtypes(exclude="object"))
        columns = []
        for i in cols:
            columns.append({"name": i})

        print("\Bivariate Analysis\U0001F447")

        while 1:
            ques = [
                {
                    "type": "checkbox",
                    "name": "col",
                    "message": "Select column for analysis",
                    "choices": columns,
                }
            ]
            ans = prompt(ques, style=self.style)
            col = ans.get("col")
            if len(col) == 2:

                dfx = self.data[col]
                ques1 = [
                    {
                        "type": "list",
                        "name": "var",
                        "message": "What do you want?",
                        "choices": [
                            "Scatter plot",
                            "Hex plot",
                            "Violin plot",
                            "BoxPlot",
                            "Correlation heat map",
                            "Simple linear regression model stats",
                            "Go Back",
                        ],
                    }
                ]
                ans1 = prompt(ques1, style=self.style)
                choice = ans1.get("var")

                if choice == "Go Back":
                    break

                elif choice == "Scatter plot":
                    fig, axes = plt.subplots(1, 2)
                    sns.scatterplot(x=col[0], y=col[1], data=dfx, ax=axes[0])
                    sns.scatterplot(x=col[1], y=col[0], data=dfx, ax=axes[1])
                    plt.show()

                elif choice == "Hex plot":
                    fig, axes = plt.subplots(1, 2)
                    dfx.plot.hexbin(x=col[0], y=col[1], gridsize=15, ax=axes[0])
                    dfx.plot.hexbin(x=col[1], y=col[0], gridsize=15, ax=axes[1])
                    plt.show()

                elif choice == "Box plot":
                    fig, axes = plt.subplots(1, 2)
                    sns.boxplot(x=col[0], y=col[1], data=dfx, ax=axes[0])
                    sns.boxplot(x=col[1], y=col[0], data=dfx, ax=axes[1])
                    plt.show()

                elif choice == "Violin plot":
                    fig, axes = plt.subplots(1, 2)
                    sns.violinplot(x=col[0], y=col[1], data=dfx, ax=axes[0])
                    sns.violinplot(x=col[1], y=col[0], data=dfx, ax=axes[1])
                    plt.show()

                elif choice == "Correlation heat map":
                    print(dfx.corr())
                    sns.heatmap(dfx.corr(), cmap="YlGnBu", annot=True)
                    plt.show()

                elif choice == "Simple linear regression model stats":
                    x1 = dfx[col[0]]
                    x1 = sm.add_constant(x1)
                    x2 = dfx[col[1]]
                    x2 = sm.add_constant(x2)
                    y1 = dfx[col[1]]
                    y2 = dfx[col[0]]
                    model1 = sm.OLS(y1, x1).fit()
                    model2 = sm.OLS(y2, x2).fit()
                    print(model1.summary())
                    print(model2.summary())
            else:
                print(
                    "\n* Choose only 2 no less and no more than 2 its Bivariate analysis! Redirecting...\n"
                )

        # Returns all the changes on the DataFrame.
        return self.data
