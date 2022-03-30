import click
import pandas as pd
from PyInquirer import prompt as piq
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PowerTransformer
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import MaxAbsScaler
from sklearn.preprocessing import QuantileTransformer

questions1 = [
    {
        'type': 'list',
        'name': 'user_option',
        'message': 'choose type of feature scaling (objects/strings  will be dropped from data frame if you use feature scaling ) - ',
        'choices': ["Not required","Normalisation/MinMaxScaling", "Standardisation/z-score", "PowerTransformer", "RobustScaler",
                    "MaxAbsScaler", "QuantileTransformer"]
    }
]
questions2 = [
    {
        'type': 'input',
        'name': 'file_name',
        'message': 'enter file name of csv file to be saved with .csv extension',
    }
]


@click.command()
@click.option('-f', prompt='enter pre processed csv file location', help='location of csv file')
def hello(f):
    """cli program to read csv file and implement feature scaling

       format: python feature.py -f 'filename.csv' """
    answers1 = piq(questions1)
    try:
        df = pd.read_csv(f)

        if answers1.get("user_option") != "Not required":
            for a in df.columns:
             if df[a].dtypes == 'object':
                df.drop([a], axis=1, inplace=True)

        if answers1.get("user_option") == "Normalisation/MinMaxScaling":
            scaler = MinMaxScaler().fit(df)
            df = pd.DataFrame(scaler.transform(df), columns=df.columns)

        elif answers1.get("user_option") == "Standardisation/z-score":
            scaler = StandardScaler().fit(df)
            df = pd.DataFrame(scaler.transform(df), columns=df.columns)

        elif answers1.get("user_option") == "PowerTransformer":
            scaler = PowerTransformer(method='yeo-johnson')
            df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

        elif answers1.get("user_option") == "RobustScaler":
            scaler = RobustScaler()
            df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

        elif answers1.get("user_option") == "MaxAbsScaler":
            scaler = MaxAbsScaler()
            df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

        elif answers1.get("user_option") == "QuantileTransformer":
            scaler = QuantileTransformer()
            df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

        answers2 = piq(questions2)
        df.to_csv(answers2.get("file_name"))
        print(df)

    except:
        print("csv file not found")


if __name__ == '__main__':
    hello()
