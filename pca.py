
from PyInquirer import style_from_dict, Token, prompt, Separator
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

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
    usr_target=''

    def __init__(self,df):
        self.df=df
        for col in self.df.columns:
           self.col_list.append(col)
        self.drop_columns()
        self.null_handler()
        self.usr_target=self.set_target()

    def drop_columns(self):
        #self.df.rename(columns=dict,inplace=True)
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
        
        ques=[
        {
            'type':'list',
            'name': 'col_name',
            'message': 'Select target column to save',
            'choices': self.col_list
        }]
        answer=prompt(ques,style=style)
        saved=answer.get('col_name')
        print(saved)
        return saved

    def pca_eigen(self):
        dict=[]
        self.col_list=[]
        for col in self.df.columns:
           self.col_list.append(col)
        for i in self.col_list:
            dict.append({'name':i})
        ques=[
        {
            'type':'checkbox',
            'name': 'cols',
            'message': 'Select the feature columns to implement PCA',
            'choices': dict
        }
        ]

        answer=prompt(ques,style=style)
        l=answer.get('cols')
        X = self.df.loc[:, l].values
        X = StandardScaler().fit_transform(X)
        pca_i1=PCA(n_components=2)
        X_transformed1 = pca_i1.fit_transform(X)
        X_centered = X - np.mean(X, axis=0)
        #cov_matrix = np.dot(X_centered.T, X_centered) 
        #eigenvalues = pca_i1.explained_variance_
        '''for eigenvalue, eigenvector in zip(eigenvalues, pca_i1.components_):    
            print('----------------------')
            print(eigenvalue)
        '''
        principalDf = pd.DataFrame(data = X_transformed1
             , columns = ['principal component 1', 'principal component 2'])
        principalDf=pd.concat([principalDf,self.df[self.usr_target]],axis=1)
        principalDf.to_csv('comp2.csv')

        #Titanic dataset specific visualization
        targets=[0,1]
        colors=['r','g']
        fig=plt.figure(figsize=[10,10],dpi=200)
        graph=fig.add_subplot(1,1,1)
        graph.set_title('2 Component PCA')
        graph.set_xlabel('Principal Component 1')
        graph.set_ylabel('Prinicipal Component 2')

        for target,color in zip(targets,colors):
            checkindex=principalDf[self.usr_target]==target
            graph.scatter(principalDf.loc[checkindex,'principal component 1'],principalDf.loc[checkindex,'principal component 2'],c=color,s=40)
        graph.legend(targets,labels=['Not Survived','Survived'])
        graph.grid()
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

