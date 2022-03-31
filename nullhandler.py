import os
from PyInquirer import style_from_dict, Token, prompt, Separator
from prompt_toolkit.validation import Validator, ValidationError
import pandas as pd
import numpy as np

def main():
    flist=[]
    for f in os.listdir():
        if f.endswith('.csv'):
            flist.append({'name':f})
    
    style = style_from_dict(
        {
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
    }
    )

    ques1=[
        {
            'type':'list',
            'name': 'file_name',
            'message': 'Select file:',
            'choices': flist,
        }
    ]
    ans1=prompt(ques1,style=style)
    file_name=ans1.get('file_name')

    df=pd.read_csv(file_name)

    df = df.replace(r'^\s*$', np.nan, regex=True)

    cols=list(df.columns)
    columns=[]
    for i in cols:
        columns.append({'name':i})
    columns.append({'name':'all'})

    choices=[
        {'name':'remove','message':"Remove all rows with null"},
        {'name':'mean','message':"Replace with mean values when possible"},
        {'name':'median','message':"Replace with median value when possible"},
        {'name':'mode','message':"Replace with mode value when possible"}
    ]
    ques2=[
        {
            'type':'checkbox',
            'name': 'col_name',
            'message': 'Select column(s):',
            'choices': columns
        },
        {
            'type':"list",
            'name':"choice",
            'message':"How do u want to handle the null values?",
            'choices':choices
        }
    ]
    ans2=prompt(ques2,style=style)
    col_name=ans2.get('col_name')
    choice=ans2.get('choice')

    if len(col_name)>1 and col_name[-1]=='all':
        col_name=list(['all'])

    if col_name[0]!='all':
        if choice=='remove':
            for i in col_name:
                df[i]=df[i].dropna()
                print(df[i].head())
        elif choice=='mean':
            for i in col_name:
                if df.dtypes[i]=='int64' or df.dtypes[i]=='float64':
                    df[i].fillna(df[i].mean(),inplace=True)
                else:
                    df[i].dropna(inplace=True)
        elif choice=='median':
            for i in col_name:
                if df.dtypes[i]=='int64' or df.dtypes[i]=='float64':
                    df[i].fillna(df[i].median(),inplace=True)
                else:
                    df[i].dropna(inplace=True)
        elif choice=='mode':
            for i in col_name:
                if df.dtypes[i]=='int64' or df.dtypes[i]=='float64':
                    df[i].fillna(df[i].mode()[0],inplace=True)
                else:
                    df[i].dropna(inplace=True)
    else:
        col_name=list(df.columns)
        if choice=='remove':
            df.dropna(inplace=True)

        elif choice=='mean':
            for i in col_name:
                if df.dtypes[i]=='int64' or df.dtypes[i]=='float64':
                    df[i].fillna(df[i].mean(),inplace=True)
                else:
                    df[i].dropna(inplace=True)
        elif choice=='median':
            for i in col_name:
                if df.dtypes[i]=='int64' or df.dtypes[i]=='float64':
                    df[i].fillna(df[i].median(),inplace=True)
                else:
                    df[i].dropna(inplace=True)
        elif choice=='mode':
            for i in col_name:
                if df.dtypes[i]=='int64' or df.dtypes[i]=='float64':
                    df[i].fillna(df[i].mode()[0],inplace=True)
                else:
                    df[i].dropna(inplace=True)

    df.to_csv(file_name[:-4]+'_new.csv')
    print("File successfuly saved")
if __name__=='__main__':
    main()
