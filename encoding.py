import pandas as pd
import click
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from data_description import DataDescription

# TODO- Need to assign classes to nullhandler and feature!
class encoding:
    tasks = [
        '1. Show categorical columns',
        '2. Performing One Hot encoding',
        '3. Show the dataset'
        # TODO -To add seperate category for ordinal variables -> map function
    ]

    def __init__(self, x):
    self.x = x

    def categoricalColumn(self):
        print('\n{0: <20}'.format("Categorical Column") + '{0: <5}'.format("Unique Values"))

        for column in self.x.select_dtypes(include="object"):
            print('{0: <20}'.format(column) + '{0: <5}'.format(self.x[column].nunique()))

    def encoding(self):
        categorical_columns = self.x.select_dtypes(include="object")

        while(1):
            column =input("Which column would you like to one hot encode?(Press -1 to go back)").lower()
            if column=="-1":
                break
            if column in categorical_columns:
                self.x = pd.get_dummies(x= self.x, columns=[column])
                print("Encoding is done")

                choice = input("Are there more columns to be encoded?(y/n)").lower()
                if choice=="y":
                    continue
                else:
                    self.categoricalColumn()
                    break
            else:
                print("Wrong column name. Try Again.")

    def categorical_main(self):
        while(1):
            print("Tasks")
            for task in self.tasks:
                print(task)
            
            while(1):
                try:
                    choice = int(input(("What you want to do? (Press -1 to go back)")))
                
                except ValueError:
                    print("Integer value required. Try Again.")
                    continue
                break

            if choice == -1:
                break
            elif choice == 1:
                self.categoricalColumn()

            elif choice == 2:
                self.categoricalColumn()
                self.encoding()

            elif choice == 3:
                DataDescription.showDataset(self)

            else:
                print("Wrong Integer value. Try again.")

        # TODO return self.x



