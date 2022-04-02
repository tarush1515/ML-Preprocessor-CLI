import os
from os.path import exists
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PyInquirer import prompt, Separator
from examples import custom_style_2 as style
from sklearn.preprocessing import MinMaxScaler, StandardScaler, PowerTransformer, RobustScaler, MaxAbsScaler, QuantileTransformer


def main():
    flist = [Separator('  csv files present in the current directory =')]
    for f in os.listdir():
        if f.endswith('.csv'):
            flist.append(f)
    flist.append(Separator(' '))
    flist.append("enter absolute path")
    flist.append("exit")
    ques1 = [
        {
            'type': 'list',
            'qmark': '*',
            'name': 'user_option',
            'message': 'Welcome to ML Preprocessor CLI! select csv file:',
            'choices': flist,
        }
    ]
    ques2 = [
        {
            'type': 'input',
            'qmark': '*',
            'name': 'file_path',
            'message': 'enter absolute path of csv file with .csv file extension:',
        }
    ]
    ans1 = prompt(ques1, style=style)

    if ans1.get("user_option") == "exit":
        exit_code()
    elif ans1.get("user_option") == "enter absolute path":
        ans2 = prompt(ques2, style=style)
        if ans2.get("file_path").endswith('.csv'):
            file_name = ans2.get("file_path")
        else:
            print("\n* Not a csv file -_- ! enter in correct format, Redirecting...\n")
            main()
    else:
        file_name = ans1.get("user_option")

    if exists(file_name):
        df = pd.read_csv(file_name)
        df = main_menu(df)
        save_file(df, file_name)
    else:
        print("\n* file doesnt exist in the entered path! Redirecting...\n")
        main()


def main_menu(df):
    questions1 = [
        {
            'type': 'list',
            'qmark': '*',
            'name': 'user_option',
            'message': 'Welcome to main menu!! what you wanna do with your data set  - ',
            'choices': [Separator(' '), Separator('  Data analyser and visualiser options! ='), "print head",
                        "dataframe basic info", "percentage of null values", "dataframe describe",
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
    answers1 = prompt(questions1, style=style)

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
        answers2 = prompt(questions2, style=style)
        if answers2.get("confirm"):
            main()
        else:
            return main_menu(df)
    elif answers1.get("user_option") == "save preprocessed data!!!":
        answers3 = prompt(questions3, style=style)
        if answers3.get("continue"):
            return df
        else:
            return main_menu(df)
    elif answers1.get("user_option") == "Force exit!":
        answers4 = prompt(questions4, style=style)
        if answers4.get("exit"):
            exit_code()
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
        print("\n* every column of dataframe is object! cant implement feature scaling! Redirecting to main menu...\n")
        return df

    questions1 = [
        {
            'type': 'checkbox',
            'qmark': '*',
            'message': 'Welcome to feature scaler! choose columns',
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
            'choices': [Separator(' '), "Yes and continue", "Yes and return to main menu", Separator(' '),
                        "No and continue",
                        "No and return to main menu"]
        }
    ]
    answers1 = prompt(questions1, style=style)
    cols = answers1.get('column_option')
    if cols:
        print(cols)
        answers2 = prompt(questions2, style=style)

        if answers2.get("feature_option") == "back":
            return feature(df)
        elif answers2.get("feature_option") == "main menu":
            return df
        else:
            answers3 = prompt(questions3, style=style)
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
        print('\n* nothing is chosen! Redirecting...\n')
        return feature(df)


def save_file(df, file_name):
    questions1 = [
        {
            'type': 'list',
            'qmark': '*',
            'name': 'user_option',
            'message': 'Choose Where you want to save preprocessed data - ',
            'choices': ["automatic generate (file is generated as initially entered file name extended with '_new')",
                        "manually enter file name "]
        }
    ]
    questions2 = [
        {
            'type': 'input',
            'qmark': '*',
            'name': 'file_path',
            'message': 'enter absolute path of csv file with .csv file extension:',
        }
    ]
    answers1 = prompt(questions1, style=style)
    if answers1.get(
            "user_option") == "automatic generate (file is generated as initially entered file name extended with '_new')":
        df.to_csv(file_name[:-4] + '_new.csv')
        print("* File successfully saved...\n")
        exit_code()
    else:
        answers2 = prompt(questions2, style=style)
        if answers2.get("file_path").endswith('.csv'):

            try:
                df.to_csv(answers2.get("file_path"))

            except:
                print("\n* absolute path in incorrect format -_- ! Redirecting...\n")
                save_file(df, file_name)
            print("* File successfully saved...\n")
            exit_code()
        else:
            print("\n* Not a csv file name -_- ! enter in correct format, Redirecting...\n")
            save_file(df, file_name)


def exit_code():
    print("Thank you for using ML Preprocessor CLI!, Have a good day...\nshutting down...")
    exit()


if __name__ == '__main__':
    main()
