import pandas as pd
from PyInquirer import prompt, Separator
from examples import custom_style_2
from sklearn.preprocessing import MinMaxScaler, StandardScaler, PowerTransformer, RobustScaler, MaxAbsScaler, \
    QuantileTransformer

df = pd.read_csv("train.csv")


def feature(df):
    a = []
    flag = 1
    for i in df.columns:
        if df[i].dtypes == 'object':
            a.append({'name': i, 'disabled': 'object'})

        else:
            a.append({'name': i})
            flag = 0
    if flag:
        print("\nevery column of dataframe is object! cant implement feature scaling! Redirecting to main menu...\n")
        return df

    questions1 = [
        {
            'type': 'checkbox',
            'qmark': '*',
            'message': 'Select columns for feature scaling\n',
            'name': 'column_option',
            'choices': a
        }
    ]
    questions2 = [
        {
            'type': 'list',
            'qmark': '*',
            'name': 'feature_option',
            'message': 'choose type of feature scaling to be applied for selected rows - ',
            'choices': ["MinMaxScaler", "StandardScaler", "PowerTransformer", "RobustScaler", "MaxAbsScaler",
                        "QuantileTransformer", Separator(' '), Separator('Menu options! ='), "back", "main menu"]
        }
    ]
    questions3 = [
        {
            'type': 'list',
            'qmark': '*',
            'name': 'user_option',
            'message': 'confirm! do you want your current chosen feature scaling  options to apply (caution!if you choose "No" data will be unchanged)',
            'choices': ["Yes and continue", "Yes and return to main menu", Separator(' '), "No and continue",
                        "No and return to main menu"]
        }
    ]

    answers1 = prompt(questions1, style=custom_style_2)
    cols = answers1.get('column_option')
    if cols:
        print(cols)
        answers2 = prompt(questions2, style=custom_style_2)

        if answers2.get("feature_option") == "back":
            return feature(df)
        elif answers2.get("feature_option") == "main menu":
            return df
        else:
            answers3 = prompt(questions3, style=custom_style_2)
            if answers3.get("user_option") == "Yes and continue":
                dfx = df[cols]
                scaler = eval(answers2.get("feature_option"))().fit(dfx)
                dfx = pd.DataFrame(scaler.transform(dfx), columns=cols)
                for j in cols:
                    df[j] = dfx[j]
                return feature(df)
            elif answers3.get("user_option") == "Yes and return to main menu":
                dfx = df[cols]
                scaler = eval(answers2.get("feature_option"))().fit(dfx)
                dfx = pd.DataFrame(scaler.transform(dfx), columns=cols)
                for j in cols:
                    df[j] = dfx[j]
                return df
            elif answers3.get("user_option") == "No and continue":
                return feature(df)
            elif answers3.get("user_option") == "No and return to main menu":
                return feature(df)
    else:
        print('\nnothing is chosen! Redirecting...\n')
        return feature(df)


df = feature(df)

print(df)
