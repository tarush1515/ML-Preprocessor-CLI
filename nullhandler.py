import os
from PyInquirer import style_from_dict, Token, prompt, Separator
from prompt_toolkit.validation import Validator, ValidationError
import pandas as pd

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
            'type':'checkbox',
            'name': 'file_name',
            'message': 'Select file:',
            'choices': flist,
            'validate': lambda ans: True if len(ans)==1
                else 'You must choose only 1 file.'
        }
    ]
    ans1=prompt(ques1,style=style)
    file_name=ans1.get('file_name')

    df=pd.read_csv(file_name[0])
    cols=list(df.columns)
    columns=[]
    for i in cols:
        columns.append({'name':i})
    columns.append({'name':'all'})

    choices=[
        {'name':'remove','message':"Remove all rows with null"},
        {'name':'mean','message':"Replace with mean values when possible"}
    ]
    ques2=[
        {
            'type':'checkbox',
            'name': 'col_name',
            'message': 'Select column(s):',
            'choices': columns
        },
        {
            'type':"checkbox",
            'name':"choice",
            'message':"How do u want to handle the null values?",
            'choices':choices
        }
    ]
    ans2=prompt(ques2,style=style)
    col_name=ans2.get('col_name')
    col_name=col_name[0]
    choice=ans2.get('choice')

    if col_name!='all':
        if choice=='remove':
            df[col_name].dropna(inplace=True)
        else:
            if df.dtypes[col_name]=='int64' or df.dtypes[col_name]=='float64':
                df[col_name].fillna(df[col_name].mean(),inplace=True)
    else:
        if choice=='remove':
            df.dropna(inplace=True)
        else:
            for i in list(df.columns):
                if df.dtypes[i]=='int64' or df.dtypes[i]=='float64':
                    df[i].fillna(df[i].mean(),inplace=True)

    df.to_csv(file_name[0].rstrip('.csv')+'_new.csv')
    print("File successfuly saved")
if __name__=='__main__':
    main()