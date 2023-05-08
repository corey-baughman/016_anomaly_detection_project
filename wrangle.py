import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, QuantileTransformer
from env import host, user, password



def get_connection(db, u=user, h=host, p=password):
    '''
    This function uses my info from my env file to
    create a connection url to access the Codeup db.
    '''
    return f'mysql+pymysql://{u}:{p}@{h}/{db}'



def new_log_data():
    '''
    This function queries the curriculum_logs database from the CodeUp MySQL server. 
    
    Arguments: None
    
    Returns: DataFrame of properties queried
    '''
    sql_query = """select date, time, path, user_id, 
                    cohort_id, name, start_date, end_date, 
                    program_id
                    from logs
                    left join cohorts
                    on logs.cohort_id = cohorts.id
                    ;
                    """
    
    # Read in DataFrame from Codeup db.
    df = pd.read_sql(sql_query, get_connection('curriculum_logs'))
    
    return df


def get_log_data():
    '''
    This function reads in curriculum_logs data from Codeup database, 
    writes data to a csv file if a local file does not exist, and 
    returns a df. Function relies on other functions in the wrangle.py module.
    '''
    if os.path.isfile('curriculum_logs.csv'):
        
        # If csv file exists read in data from csv file.
        df = pd.read_csv('curriculum_logs.csv', index_col=0)
        
    else:
        
        # Read fresh data from db into a DataFrame
        df = new_log_data()
        
        # Cache data
        df.to_csv('curriculum_logs.csv')
        
    return df


def wrangle_log_data():
    '''
    This function retrieves the curriculum_log data from the CodeUp MySQL database. 
    It adds the feature 'date_time' and establishes that as the index. It returns the 
    cleaned dataframe. Function relies on other functions in the wrangle.py module.
    '''
    # acquiring data from SQL server
    df = get_log_data()
    # adding a date_time feature that is the concatenation of 'date' and 'time'.
    df['date_time'] = df.date + ' ' + df.time
    # casting 'datetime' to a datetime dtype
    df['date_time'] = pd.to_datetime(df['date_time'])
    # setting date_time to index and sorting index
    df = df.set_index('date_time').sort_index()
    # there are some users without cohort and it's resulting start/end dates, name
    # and program_id. Going to fill those fields appropriately
    # 9999-01-01
    df.name = df.name.fillna('None Assigned')
    df.program_id = df.program_id.fillna(999).astype('int')
    df.start_date = df.start_date.fillna('1999-01-01')
    df.end_date = df.end_date.fillna('1999-01-01')
    df.cohort_id = df.cohort_id.fillna(999).astype('int')
    df.start_date = pd.to_datetime(df.start_date)
    df.end_date = pd.to_datetime(df.end_date)
    # there is one null value in path,
    # replacing that with 'no_path_recorded'
    df.fillna('no_path_recorded', inplace=True)
    
    return df



'''
col_list establishes a list of columns with significant outliers as
discovered in univariate analysis. These are primarily right skewed
(very large high-end properties). This model is to predict assessed tax
values of homes, so it seems best to have it perform well on the vast
majority of properties instead of the outliers which, like fine art,
have a much less regular connection to normal market parameters and 
would likely distort the model.
'''
col_list = ['bedrooms', 'bathrooms', 'area', 'tax_value', 'tax_amount', 'tax_value_2016']



def remove_outliers(df, col_list=col_list, k=1.5):
    '''
    remove outliers from a dataframe based on a list of columns
    using the tukey method.
    
    Arguments: a DataFrame, col_list=[list of column names or indexes]
                , a k value that equals the number of InterQuartile Ranges
                outside of Q1 and Q3 that will define outliers to be removed.
                col_list defaults to the col_list variable in this module.
                k defaults to the standard 1.5 * IQR for Tukey method.
                
    Returns: a single dataframe with outliers removed
    '''
    col_qs = {}
    for col in col_list:
        col_qs[col] = q1, q3 = df[col].quantile([0.25, 0.75])
    for col in col_list:
        iqr = col_qs[col][0.75] - col_qs[col][0.25]
        lower_fence = col_qs[col][0.25] - (k*iqr)
        upper_fence = col_qs[col][0.75] + (k*iqr)
        df = df[(df[col] > lower_fence) & (df[col] < upper_fence)]
    df.reset_index(drop=True, inplace=True)
    
    return df



    
    