import pandas as pd
from data_analysis import DataAnalysis
from PyInquirer import prompt


class Imputation:

    bold_start = "\033[1m"
    bold_end = "\033[0;0m"

    def __init__(self, data, style):
        self.data = data
        self.style = style

    # function to show columns of the DataFrame
    def showColumns(self):
        print("\nColumns\U0001F447\n")
        for column in self.data.columns.values:
            print(column, end="  ")
        print("\n")
        return

    # function to print the number of NULL values present in each column
    def printNullValues(self):
        print("\nNULL values of each column:")
        for column in self.data.columns.values:
            # isnull checks on each value of a column that whether the value is null or not.
            print(
                "{0: <20}".format(column)
                + "{0: <5}".format(sum(pd.isnull(self.data[column])))
            )
        print("")
        return

    # function to remove a column from the DataFrame
    def removeColumn(self):
        self.showColumns()
        cols = list(self.data.columns)
        columns = []
        for i in cols:
            columns.append({"name": i})
        while 1:

            ques1 = [
                {
                    "type": "checkbox",
                    "name": "delete_col",
                    "message": "Select the columns you want to delete",
                    "choices": columns,
                },
            ]
            ans1 = prompt(ques1, style=self.style)
            delete_col = ans1.get("delete_col")

            self.data.drop(labels=delete_col, axis=1, inplace=True)

            return

    # function that fills null values with the mean of that column.
    def fillNullWithMean(self):

        cols = list(self.data.columns)
        columns = []
        for i in cols:
            columns.append({"name": i})

        ques1 = [
            {
                "type": "list",
                "name": "col",
                "message": "Select the columns you want to fill with mean",
                "choices": columns,
            },
        ]
        ans1 = prompt(ques1, style=self.style)
        col = ans1.get("col")
        try:
            self.data[col] = self.data[col].fillna(self.data[col].mean())
        except TypeError:
            # Imputation is only possible on some specific datatypes like int, float etc.
            print(
                "The Imputation is not possible here\U0001F974. Try on another column."
            )
        print("Done......\U0001F601")
        return

    # function that fills null values with the median of that column.
    def fillNullWithMedian(self):
        cols = list(self.data.columns)
        columns = []
        for i in cols:
            columns.append({"name": i})

        ques1 = [
            {
                "type": "list",
                "name": "col",
                "message": "Select the columns you want to fill with mean",
                "choices": columns,
            },
        ]
        ans1 = prompt(ques1, style=self.style)
        col = ans1.get("col")
        try:
            self.data[col] = self.data[col].fillna(self.data[col].median())
        except TypeError:
            # Imputation is only possible on some specific datatypes like int, float etc.
            print(
                "The Imputation is not possible here\U0001F974. Try on another column."
            )
        print("Done......\U0001F601")
        return

    # function that fills null values with the mode of that column.
    def fillNullWithMode(self):
        cols = list(self.data.columns)
        columns = []
        for i in cols:
            columns.append({"name": i})

        ques1 = [
            {
                "type": "list",
                "name": "col",
                "message": "Select the columns you want to fill with mean",
                "choices": columns,
            },
        ]
        ans1 = prompt(ques1, style=self.style)
        col = ans1.get("col")
        try:
            self.data[col] = self.data[col].fillna(self.data[col].mode())
        except TypeError:
            # Imputation is only possible on some specific datatypes like int, float etc.
            print(
                "The Imputation is not possible here\U0001F974. Try on another column."
            )
        print("Done......\U0001F601")
        return

    # main function of the Imputation Class.
    def imputer(self):
        print("\nImputation Tasks\U0001F447\n")

        choices = [
            "Show number of Null Values",
            "Remove Columns",
            "Fill Null Values (with mean)",
            "Fill Null Values (with median)",
            "Fill Null Values (with mode)",
            "Show the Dataset",
            "Go Back",
        ]

        while 1:
            ques = [
                {
                    "type": "list",
                    "name": "choice",
                    "message": "What you want to do?",
                    "choices": choices,
                },
            ]
            ans = prompt(ques, style=self.style)
            choice = ans.get("choice")

            if choice == "Go Back":
                break

            elif choice == "Show number of Null Values":
                self.printNullValues()

            elif choice == "Remove Columns":
                self.removeColumn()

            elif choice == "Fill Null Values (with mean)":
                self.fillNullWithMean()

            elif choice == "Fill Null Values (with median)":
                self.fillNullWithMedian()

            elif choice == "Fill Null Values (with mode)":
                self.fillNullWithMode()

            elif choice == "Show the Dataset":
                DataDescription.showDataset(self)

        return self.data
