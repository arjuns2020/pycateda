# Importing Packages
import warnings
import missingno as msno
import time
import calendar
import os
from pandas_profiling import ProfileReport
import seaborn as sns
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
pd.options.display.max_columns = None
pd.options.display.max_rows = None
sns.set_style("whitegrid")
warnings.filterwarnings("ignore")
########################################################################################

# read a csv file and return a dataframe


def read_csv(fn):
    '''reads a csv file and returns a pandas dataframe'''
    temp = pd.read_csv(fn)
    return pd.DataFrame(temp)

# Descriptive Statistics of the data


def Summary_Data(df):
    '''
    the function below is a general EDA of a dataset
    Usage -> Summary_Data(dataframe)

    '''
    t0 = time.time()
    # head of dataset
    print('\n ##########---> head of data <--- ##########')
    print(df.head())

    # tail of dataset
    print(' \n ##########--->  tail of data <--- ##########')
    print(df.tail())

    # check the shape of data
    print('\n ##########---> shape of data <--- ##########')
    print(df.shape)

    # check missing values
    print('\n ##########---> check missing values <--- ##########')
    print(df.isnull().sum())

    # check duplicated rows
    print('\n ##########---> checking duplicated rows <--- ##########')
    print(df[df.duplicated()].shape)

    # check the data type of columns
    print('\n ##########---> data type <--- ##########')
    print(df.dtypes)

    # generate descriptive statistics
    print('\n ##########--->  generate descriptive statistics <--- ##########')
    # numerical features
    print(round(df.describe(), 2))
    # categorical features
    print(round(df.describe(include=[np.object]), 2))

    # # check number of unique values for each feature

    print('\n ##########--->  number of unique values <--- ##########')
    n_unique = df.nunique().tolist()
    print(df.nunique())

    # find the unique identifier
    print('\n ##########---> find the unique identifier <--- ##########')
    for i in range(df.shape[1]):
        if n_unique[i] == len(df):
            print("{} is the unique identifier".format(df.columns[i]))

    df.dropna(axis=1, inplace=True, how='all')

    # print unique values
    print('\n ##########--->  unique values for each feature =======')
    for col in df.columns:
        if df[col].dtypes.name == 'object' or df[col].dtypes.name == 'category':
            if df[col].nunique() < 100:
                print('column name:', col)
                print(df[col].unique())
                print('\n --------------------------------')
            else:
                print(f'over 100 unique values in {col}...')

    # print relative frequency (%) of unique values or bins of numerical features
    print('\n ##########---> relative frequency (precentage) of unique values or bins of numerical features <--- ##########')
    for col in df.columns:

        if df[col].dtypes.name == 'object' or df[col].dtypes.name == 'category':
            print(f"{col} -- categorical feature; top 20 categories")
            print(round(df[col].value_counts(normalize=True)*100, 2)[:20])
        else:
            print(f"{col} -- numerical feature; 5 bins")
            print(round(df[col].value_counts(bins=5)))
        print(' \n ---------------END--------------')

    print('time took to Analyse is %.2f seconds' % (time.time()-t0))


# Count the number of null values in the dataframe


def Null_Counts(df1):
    nulls_df = pd.DataFrame(df1.isnull().sum(), columns=['Null Count'])
    return nulls_df

# Print % of missing values in each columns in a dataframe


def Null_Percents(df1):
    # make a list of the variables that contain missing values
    vars_with_na = [var for var in df1.columns if df1[var].isnull().sum() > 1]

    # print the variable name and the percentage of missing values
    for var in vars_with_na:
        print(var, np.round(df1[var].isnull().mean(), 3),  ' % missing values')


# Shows Missing Values Plots of entire dataframe
def Plot_Missing_Value(df1):
    return msno.matrix(df1)


# Build Profile Report of the entire dataset

def EDA_Report(df, report_name):
    '''
    the function below is a general EDA of a dataset
    EDA_Report(DataFrameName, 'Report Name')
    '''
    t0 = time.time()
    if not os.path.exists("reports"):
        os.makedirs("reports")

    filename = os.path.join('reports', report_name.replace(' ', '_').lower()
                            + "_"+str(calendar.timegm(time.gmtime()))+".html")
    profile = ProfileReport(df, title=report_name)
    profile.to_file(filename)
    print('time took to generate report is %.2f seconds' % (time.time()-t0))
    return profile


# list of numerical variables

def Show_Numerical_Variables(df):
    num_vars = [var for var in df.columns if df[var].dtypes != 'O']
    return df[num_vars].head(10)
    #print('Number of numerical variables: ', len(num_vars))
    # return the numerical variables top 10 rows

#  list of discrete variables


def Show_Descrete_Variables(df):
    if len(df) > 1:
        # get a list of all numerical valiables
        num_vars = [var for var in df.columns if df[var].dtypes != 'O']
        # check in the numerical variables for categorical condition
        discrete_vars = [var for var in num_vars if len(df[var].unique()) < 20]
        return df[discrete_vars].head(10)
    else:
        print('No data in Data Frame')

# List of Contineous Variables


def Show_Contineous_Variables(df):
    # Numerical Variables
    num_vars = [var for var in df.columns if df[var].dtypes != 'O']
    # discrete variables
    discrete_vars = [var for var in num_vars if len(df[var].unique()) < 20]
    # list of continuous variables
    cont_vars = [var for var in num_vars if var not in discrete_vars]
    return df[cont_vars].head(10)


def Analyse_continuous_Variables(df):
    # Numerical Variables
    num_vars = [var for var in df.columns if df[var].dtypes != 'O']
    # discrete variables
    discrete_vars = [var for var in num_vars if len(df[var].unique()) < 20]
    # list of continuous variables
    cont_vars = [var for var in num_vars if var not in discrete_vars]

    for var in cont_vars:
        print(var, len(df[var].unique()), ' categories')

    for var in cont_vars:
        df[var].hist(bins=20, edgecolor='black')
        plt.ylabel('Numbers')
        plt.xlabel(var)
        plt.title(var)
        plt.show()


def Analyse_log_continuous_Variables(df):
    num_vars = [var for var in df.columns if df[var].dtypes != 'O']
    # discrete variables
    discrete_vars = [var for var in num_vars if len(df[var].unique()) < 20]
    # list of continuous variables
    cont_vars = [var for var in num_vars if var not in discrete_vars]

    for var in cont_vars:
        if 0 in df[var].unique():
            pass
        else:
            df[var] = np.log(df[var])
            df[var].hist(bins=20, edgecolor='black')
            plt.ylabel('Numbers')
            plt.xlabel(var)
            plt.title(var)
            plt.show()


def Analyse_Outliers(df):
    num_vars = [var for var in df.columns if df[var].dtypes != 'O']
    # discrete variables
    discrete_vars = [var for var in num_vars if len(df[var].unique()) < 20]
    # list of continuous variables
    cont_vars = [var for var in num_vars if var not in discrete_vars]

    for var in cont_vars:
        if 0 in df[var].unique():
            pass
        else:
            df[var] = np.log(df[var])
            df.boxplot(column=var)
            plt.title(var)
            plt.ylabel(var)
            plt.show()
