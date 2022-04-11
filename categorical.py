import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from data_analysis import DataAnalysis
from PyInquirer import prompt


class Categorical:
    # The Task associated with this class.

    def __init__(self, data, style):
        self.data = data
        self.style = style

    # function to show all the categorical columns and number of unique values in them.
    def categoricalColumn(self):
        print(
            "\n{0: <20}".format("Categorical Column")
            + "{0: <5}".format("Unique Values")
        )
        # select_dtypes selects the columns with object datatype(which could be further categorize)
        for column in self.data.select_dtypes(include="object"):
            print(
                "{0: <20}".format(column)
                + "{0: <5}".format(self.data[column].nunique())
            )

    # function to one hot encode any particular column
    def one_hot_encoding(self):
        categorical_columns = self.data.select_dtypes(include="object")
        print(categorical_columns)
        while 1:
            ques = [
                {
                    "type": "list",
                    "name": "cat_col",
                    "message": "Which column would you like to one hot encode?",
                    "choices": categorical_columns,
                },
            ]
            ans = prompt(ques, style=self.style)
            cat_col = ans.get("cat_col")

            # The encoding function is only for categorical columns.
            if cat_col in categorical_columns:
                self.data = pd.get_dummies(data=self.data, columns=[cat_col])
                print("One Hot Encoding is done.......\U0001F601")
            return

    # function to label encode any particular column
    def labelEncoding(self):
        categorical_columns = self.data.select_dtypes(include="object")
        while 1:
            ques = [
                {
                    "type": "list",
                    "name": "cat_col",
                    "message": "Which column would you like to label encode?",
                    "choices": categorical_columns,
                },
            ]
            ans = prompt(ques, style=self.style)
            cat_col = ans.get("cat_col")

            # The encoding function is only for categorical columns.
            if cat_col in categorical_columns:
                class_1e = LabelEncoder()
                self.data[cat_col] = class_1e.fit_transform(self.data[cat_col].values)
                print("Label Encoding is done.......\U0001F601")
            return

    # The main function of the Categorical class.
    def categoricalMain(self):
        print("\nTasks\U0001F447")
        # for task in self.tasks:
        #     print(task)
        choices = [
            "Show Categorical Columns",
            "Perform One Hot encoding",
            "Perform Label encoding",
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

            elif choice == "Show Categorical Columns":
                self.categoricalColumn()

            elif choice == "Perform One Hot encoding":
                self.categoricalColumn()
                self.one_hot_encoding()

            elif choice == "Perform Label encoding":
                self.categoricalColumn()
                self.labelEncoding()

            elif choice == "Show the Dataset":
                DataDescription.showDataset(self)

        # return the data after modifying
        return self.data
