from data_analysis import DataAnalysis
from data_input import DataInput
from imputation import Imputation
from download import Download
from categorical import Categorical
from feature_scaling import FeatureScaling
from pca2 import pca
from PyInquirer import style_from_dict, Token, prompt, Separator
import pyfiglet
import pandas as pd

class Preprocessor:

    data = 0
    targetdf=pd.DataFrame()
    style = style_from_dict(
        {
            Token.Separator: "#cc5454",
            Token.QuestionMark: "#673ab7 bold",
            Token.Selected: "#cc5454",  # default
            Token.Pointer: "#673ab7 bold",
            Token.Instruction: "",  # default
            Token.Answer: "#f44336 bold",
            Token.Question: "",
        }
    )

    preprocessing_choices = [
        "Data Analysis",
        "Handling NULL Values",
        "Encoding Categorical Data",
        "Feature Scaling of the Dataset",
        "Perform PCA",
        "Download the modified dataset",
        "Exit",
    ]

    def __init__(self):
        self.data = DataInput().inputFunction()
        
        print(pyfiglet.figlet_format("Welcome  to\nML  Preprocessor CLI  !  !  !"))
        self.targetdf=self.preprocessorMain()

    # function to remove the target column of the DataFrame.
    def removeTargetColumn(self):

        cols = list(self.data.columns)
        columns = []
        for i in cols:
            columns.append({"name": i})

        ques = [
            {
                "type": "list",
                "name": "target",
                "message": "Select your target variable\n",
                "choices": columns,
            }
        ]
        ans = prompt(ques, style=self.style)
        target = ans.get("target")
        self.targetdf=self.data[target]
        print("Done.......\U0001F601")
        return 

    # prints data
    def printData(self):
        print(self.data)

    # main function of the Preprocessor class.
    def preprocessorMain(self):
        self.removeTargetColumn()

        print("\nTasks (Preprocessing)\U0001F447\n")
        while 1:
            ques = [
                {
                    "type": "list",
                    "name": "task",
                    "message": "What do you want to do?\n",
                    "choices": self.preprocessing_choices,
                }
            ]
            ans = prompt(ques, style=self.style)
            task = ans.get("task")

            if task == "Exit":
                print("Thank You for using ML Preprocessor CLI\U0001F601")
                exit()

            # moves the control into the DataAnalysis class.
            elif task == "Data Analysis":
                DataAnalysis(self.data, self.style).describe()

            # moves the control into the Imputation class.
            elif task == "Handling NULL Values":
                self.data = Imputation(self.data, self.style).imputer()

            # moves the control into the Categorical class.
            elif task == "Encoding Categorical Data":
                self.data = Categorical(self.data, self.style).categoricalMain()

            # moves the control into the FeatureScaling class.
            elif task == "Feature Scaling of the Dataset":
                self.data = FeatureScaling(self.data, self.style).scaling()
            
            #moves the control into PCA class
            elif task == "Perform PCA":
                self.data= pca(self.data)
                self.data.pca_eigen()
            
            # moves the control into the Download class.
            elif task == "Download the modified dataset":
                Download(self.data, self.style).download()


obj = Preprocessor()

