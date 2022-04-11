
from PyInquirer import style_from_dict, Token, prompt, Separator
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from prompt_toolkit.validation import Validator, ValidationError

class NumberValidator(Validator):

    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(message="Please enter a number",
                                  cursor_position=len(document.text))


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

class pca:
    
    col_list=[]
    usr_target=pd.DataFrame()
    target_name=''
    df_pca=pd.DataFrame()

    def __init__(self,df):
        self.df=df
        for col in self.df.columns:
           self.col_list.append(col)
        self.drop_columns()
        self.null_handler()
        self.usr_target=self.set_target()
        #self.df.drop(['target'],axis=1,inplace=True)

    def drop_columns(self):
        dict=[]
        for i in self.col_list:
            dict.append({'name':i})
        ques=[
        {
            'type':'checkbox',
            'name': 'cols',
            'message': 'Select the redundant colums to drop them',
            'choices': dict
        }
        ]

        answer=prompt(ques,style=style)
        l=answer.get('cols')
        print('Dropping ',l)
        self.df.drop(l,axis=1,inplace=True)
        return self.df


    def set_target(self):
        dict=[]
        for i in self.df.columns:
            dict.append({'name':i})
        ques=[
        {
            'type':'list',
            'name': 'col_name',
            'message': 'Select target column to save',
            'choices': dict
        }]
        answer=prompt(ques,style=style)
        self.target_name=answer.get('col_name')
        self.df.rename(columns={self.target_name: 'target'}, inplace=True)
        return self.df['target']
    
    def pca_eigen(self):
        '''ques=[
        {
            'type': "input",
            "name": "n",
            "message": "Enter no of components to keep after reduction",
            "validate": NumberValidator,
            "filter": lambda val: int(val)
        }
        ]

        answer=prompt(ques,style=style)
        n=answer.get('n')
        while n>7:
            print('Please enter <=7 components')
            answer=prompt(ques,style=style)
            n=answer.get('n')
        '''
        self.df=self.df.apply(LabelEncoder().fit_transform)
        X = self.df.values
        X = StandardScaler().fit_transform(X)
        pca_i1=PCA(n_components=2)
        X_transformed1 = pca_i1.fit_transform(X)
        #X_centered = X - np.mean(X, axis=0)
        #cov_matrix = np.dot(X_centered.T, X_centered) 
        #eigenvalues = pca_i1.explained_variance_
        '''for eigenvalue, eigenvector in zip(eigenvalues, pca_i1.components_):    
            print('----------------------')
            print(eigenvalue)
        '''
        principalDf = pd.DataFrame(data = X_transformed1, columns = ['principal component 1', 'principal component 2'])
        principalDf=pd.concat([principalDf,self.usr_target],axis=1)
        ques=[{'type':'input','name':'fname','message':'enter name of .csv file to save eigen values'}]
        ans=prompt(ques,style=style)
        ans=ans.get('fname')
        principalDf.to_csv(ans+'.csv')

        labels=[]

        for i in list(principalDf.target.unique()):
            labels.append(i)
        
        if labels[0]==np.nan:
            labels.pop(0)
        colors=['r','g','b','y','k','m','c']
        colors=colors[:len(labels)]
        fig=plt.figure(figsize=[10,10],dpi=150)
        graph=fig.add_subplot(1,1,1)

        graph.set_title('2 Component PCA')
        graph.set_xlabel('Principal Component 1')
        graph.set_ylabel('Prinicipal Component 2')

        for target,color in zip(labels,colors):
            checkindex=principalDf['target']==target
            graph.scatter(principalDf.loc[checkindex,'principal component 1'],principalDf.loc[checkindex,'principal component 2'],c=color,s=40)
        
        graph.legend(labels,labels=labels)
        plt.show()
        fig.savefig('pca.png',bbox_inches='tight')

    def null_handler(self):
    
        self.df = self.df.replace(r'^\s*$', np.nan, regex=True)   #replacing empty spaces as numpy null NaN

        cols=list(self.df.columns)
        columns=[]
        for i in cols:
            columns.append({'name':i})
        columns.append({'name':'all'})
        print('{:^80s}'.format("NULL HANDLING"))

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
                'message': 'Select column(s) to handle the null values:',
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
                    self.df[i].dropna(inplace=True)
            elif choice=='mean':
                for i in col_name:
                    if self.df.dtypes[i]=='clistnt64' or self.df.dtypes[i]=='float64':
                        self.df[i].fillna(self.df[i].mean(),inplace=True)
                    else:
                        self.df[i].dropna(inplace=True)
            elif choice=='median':
                for i in col_name:
                    if self.df.dtypes[i]=='int64' or self.df.dtypes[i]=='float64':
                        self.df[i].fillna(self.df[i].median(),inplace=True)
                    else:
                        self.df[i].dropna(inplace=True)
            elif choice=='mode':
                for i in col_name:
                    if self.df.dtypes[i]=='int64' or self.df.dtypes[i]=='float64':
                        self.df[i].fillna(self.df[i].mode()[0],inplace=True)
                    else:
                        self.df[i].dropna(inplace=True)
        else:
            col_name=list(self.df.columns)
            if choice=='remove':
                self.df.dropna(inplace=True)

            elif choice=='mean':
                for i in col_name:
                    if self.df.dtypes[i]=='int64' or self.df.dtypes[i]=='float64':
                        self.df[i].fillna(self.df[i].mean(),inplace=True)
                    else:
                        self.df[i].dropna(inplace=True)
            elif choice=='median':
                for i in col_name:
                    if self.df.dtypes[i]=='int64' or self.df.dtypes[i]=='float64':
                        self.df[i].fillna(self.df[i].median(),inplace=True)
                    else:
                        self.df[i].dropna(inplace=True)
            elif choice=='mode':
                for i in col_name:
                    if self.df.dtypes[i]=='int64' or self.df.dtypes[i]=='float64':
                        self.df[i].fillna(self.df[i].mode()[0],inplace=True)
                    else:
                        self.df[i].dropna(inplace=True)
