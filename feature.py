import pandas as pd
from PyInquirer import prompt, Separator
from examples import custom_style_2
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, StandardScaler, PowerTransformer, RobustScaler, MaxAbsScaler, QuantileTransformer

df = pd.read_csv("train.csv")


def main_menu(df):
    questions1 = [
        {
            'type': 'list',
            'qmark': '*',
            'name': 'user_option',
            'message': 'welcome to main menu!! what you wanna do with your data set  - ',
            'choices': [Separator(' '), Separator('  Data analyser and visualiser options! ='), "print head", "dataframe basic info", "percentage of null values", "dataframe describe",
                        "dataframe correlation with heatmap", Separator(' '), Separator('  preprocessing options! ='),
                        "nullhandler", "character encoder", "feature scaler",
                        Separator(' '), Separator('  menu options! ='), "discard current work and start new(caution!)",
                        "save preprocessed data!!!", "Force exit!"]
        }
    ]
    questions2 = [
        {
            'type': 'confirm',
            'qmark': '#',
            'message': 'confirm! Do you want to continue with discarding current work and start new?',
            'name': 'confirm',
            'default': False,
        }
    ]
    questions3 = [
        {
            'type': 'confirm',
            'qmark': '#',
            'message': 'Do you want to continue with saving file?(make sure you are completed with preprocessing)',
            'name': 'continue',
            'default': False,
        }
    ]
    questions4 = [
        {
            'type': 'confirm',
            'qmark': '#',
            'message': 'Do you want to force exit?',
            'name': 'exit',
            'default': False,
        }
    ]
    answers1 = prompt(questions1, style=custom_style_2)

    if answers1.get("user_option") == "print head":
        print(df.head(10))
        return main_menu(df)
    elif answers1.get("user_option") == "dataframe basic info":
        df.info()
        return main_menu(df)
    elif answers1.get("user_option") == "percentage of null values":
        print(df.isnull().mean() * 100)
        return main_menu(df)
    elif answers1.get("user_option") == "dataframe describe":
        print(df.describe(include='all'))
        return main_menu(df)
    elif answers1.get("user_option") == "dataframe correlation with heatmap":
        print(df.corr())
        sns.heatmap(df.corr(), cmap="YlGnBu", annot=True)
        plt.show()
        return main_menu(df)
    elif answers1.get("user_option") == "nullhandler":
        # df = nullhandler(df)
        return main_menu(df)
    elif answers1.get("user_option") == "character encoder":
        # df = character_encoder(df)
        return main_menu(df)
    elif answers1.get("user_option") == "feature scaler":
        df = feature(df)
        return main_menu(df)
    elif answers1.get("user_option") == "discard current work and start new(caution!)":
        answers2 = prompt(questions2, style=custom_style_2)
        if answers2.get("confirm"):
            # main()
            return main_menu(df)  # remove after creating main file
        else:
            return main_menu(df)
    elif answers1.get("user_option") == "save preprocessed data!!!":
        answers3 = prompt(questions3, style=custom_style_2)
        if answers3.get("continue"):
            return df
        else:
            return main_menu(df)
    elif answers1.get("user_option") == "Force exit!":
        answers4 = prompt(questions4, style=custom_style_2)
        if answers4.get("exit"):
            print("Have a good day...\nshutting down...")
            exit()
        else:
            return main_menu(df)


def feature(df):
    a = [Separator(' '), Separator(' Select columns for feature scaling =')]


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
            'message': 'welcome to feature scaler!\n',
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
                        "QuantileTransformer", Separator(' '), Separator('  Menu options! ='), "back", "main menu"]
        }
    ]
    questions3 = [
        {
            'type': 'list',
            'qmark': '#',
            'name': 'user_option',
            'message': 'confirm! do you want your current chosen feature scaling  options to apply (caution!if you choose "No" data will be unchanged) - ',
            'choices': [Separator(' '), "Yes and continue", "Yes and return to main menu", Separator(' '), "No and continue",
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
                return df
    else:
        print('\nnothing is chosen! Redirecting...\n')
        return feature(df)


df = main_menu(df)
print(df)
