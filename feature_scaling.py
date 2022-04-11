import pandas as pd
from data_analysis import DataAnalysis
from sklearn.preprocessing import MinMaxScaler, StandardScaler, PowerTransformer, RobustScaler, MaxAbsScaler, QuantileTransformer
from PyInquirer import prompt, Separator


class FeatureScaling:

    def __init__(self, data, style):
        self.data = data
        self.style = style

    # main function of the FeatureScaling Class.
    def scaling(self):
        scaling_col = list(self.data.select_dtypes(exclude="object"))
        columns = []
        for i in scaling_col:
            columns.append({"name": i})

        print("\nTasks (Feature Scaling)\U0001F447")

        while 1:
            ques = [
                {
                    "type": "checkbox",
                    "name": "cols",
                    "message": "Select columns for feature scaling ",
                    "choices": columns,
                }
            ]
            ans = prompt(ques, style=self.style)
            cols = ans.get("cols")
            ques1 = [
                {
                    "type": "list",
                    "name": "scaling_type",
                    "message": "Choose type of feature scaling",
                    "choices": [
                        "MinMaxScaler",
                        "StandardScaler",
                        "PowerTransformer",
                        "RobustScaler",
                        "MaxAbsScaler",
                        "QuantileTransformer",
                        Separator(" "),
                        "Go Back",
                    ],
                }
            ]
            ans1 = prompt(ques1, style=self.style)
            choice = ans1.get("scaling_type")

            print(choice)

            if choice == "Go Back":
                break

            elif choice == "Show the Dataset":
                DataDescription.showDataset(self)

            else:
                scaler = eval(choice)().fit(self.data[cols])
                self.data[cols] = pd.DataFrame(
                    scaler.transform(self.data[cols]), columns=cols
                )
                print("Scaling Done...👍")
                break
        # Returns all the changes on the DataFrame.
        return self.data
