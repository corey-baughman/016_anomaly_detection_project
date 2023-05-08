# explore.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# visualize the top lessons by cohort v. the top lesson for cohort's program
def viz_top_lessons(df):
    '''
    This function takes in a df and list of cohorts and makes vizualtions
    of the top paths for each cohort against the average top paths for the
    program id.
    Aguments: df, the dataframe of the program_id
                cohorts, a list of the cohorts in the program
    Returns: Nothing. Displays visualizations.
    '''
    # create cohort list
    cohorts = df.name.unique().tolist()
    # list of non-lesson paths
    not_lessons = ['/', 'search/search_index.json', 'toc', 'index.html', 'appendix']
    # make dataframes with only lesson paths:
    lessons = df[~df.path.isin(not_lessons)]
    # top lessons for whole program id
    top_lessons = pd.DataFrame(
            lessons.value_counts('path', normalize=True).head(), 
            columns=['proportion_ttl_views']).reset_index()
    # create visualization for each cohort
    for cohort in cohorts:
        df = lessons[lessons.name == cohort]
        cohort_top_lessons = pd.DataFrame(
            df.value_counts('path', normalize=True).head(), 
            columns=['proportion_ttl_views']).reset_index()
        if cohort_top_lessons.shape[0] >= 5:
            # now plot that against each cohort's top lessons
            top_lessons.plot.bar(x='path', y='proportion_ttl_views', alpha=.5)
            plt.title('Proportion of Total Views by Path')
            plt.xlabel('Path')
            plt.ylabel('Proportion of Total Views')
            plt.show()
            cohort_top_lessons.plot.bar(x='path', y='proportion_ttl_views', alpha=.5)
            plt.title(f'Proportion of Total Views by Path for Cohort {cohort}')
            plt.xlabel('Path')
            plt.ylabel('Proportion of Total Views')
            plt.show()
            print('==============================================================\n\n')
        else:
            print(f'Cohort {cohort} does not have enough paths to compare.')

            
# find top lessons for a program id
def top_lessons_by_program(df):
    '''
    function takes in a dataframe and returns the top lesson paths 
    visited by program cohorts.
    Arguments: A DataFrame from curriculum_logs db
    Returns: DataFrame of top lessons for the input df.'''
    # list of non-lesson paths
    not_lessons = ['/', 'search/search_index.json', 'toc', 'index.html', 'appendix']
    # make dataframes with only lesson paths:
    lessons = df[~df.path.isin(not_lessons)]
    top_lessons = pd.DataFrame(
            lessons.value_counts('path', normalize=True).head(), 
            columns=['proportion_ttl_views']).reset_index()
       
    return top_lessons

    
# find top lessons for a program id after being active students
def top_lessons_after_active(df):
    '''
    function takes in a dataframe and returns the top lesson paths 
    visited by program after cohorts were no longer active students.
    Arguments: A DataFrame from curriculum_logs db
    Returns: DataFrame of top lessons post-active students for the input df.'''
    # list of non-lesson paths
    not_lessons = ['/', 'search/search_index.json', 'toc', 'index.html', 'appendix']
    # make dataframes with only lesson paths:
    lessons = df[~df.path.isin(not_lessons)]
    lessons = lessons[lessons.end_date < lessons.index]
    top_lessons = pd.DataFrame(
            lessons.value_counts('path', normalize=True).head(), 
            columns=['proportion_ttl_views']).reset_index()
        
    return top_lessons


# create a df of logs by active users:
def get_active_user_logs(df):
    '''
    takes in a curriculum log dataframe and returns the df filtered to 
    only log entries that took place while students were active
    '''
    df = df[(df.start_date < df.index) & (df.end_date > df.index)]
    
    return df


# make a column for 'hardly accesses curriculum'.
# column can be based on a variable percentage of the mean for their
# program.
def low_usage_users(df, n):
    '''
    This function takes in a curriculum logs dataframe and returns
    a dataframe of users who use the curriculum at a rate of n times
    the mean for all users in the dataset or less.
    
    Arguments: df: a curriculum logs dataframe
                n: an integer or float value representing the desired 
                number of times the mean usage to define as low_usage
    Returns: original df with added columns 'total_visits' which represents
            how many log entries the individual user made, and 'hardly_used'
            which represents whether a user was at or below the threshold
            value of vists as establish by n * mean_usage.
    '''
    # establish mean_usage for all users in df
    mean_usage = df.groupby('user_id').count().path.mean()
    # create a df of for users visit data
    users_df = []
    # create df for each user and append to users_df
    for user in df.user_id.unique():
        user_df = df[df.user_id == user]
        total_visits = user_df.shape[0]
        hardly_used = total_visits <= (mean_usage * n)
        user_df = user_df.assign(total_visits=total_visits, hardly_used=hardly_used)
        users_df.append(user_df)
    # concatenate all of the user_df in users_df
    df = pd.concat(users_df)
    # return a df of users meeting the 'hardly_used' description
    return df[df.hardly_used == True]


# creates df of users who logged only n% or less paths compared to paths
# logged by the average user.
def low_users_by_cohort(df, n=0.1):
    '''
    Function takes in a dataframe of curriculum logs and returns
    a dataframe of low curriculum users by cohort. Relies on the
    low_usage_users function.
    
    Arguments: df: a curriculum logs dataframe
                n: an integer or float value representing the desired 
                number of times the mean usage to define as low_usage
    Returns: df of low curriculum users by cohort which represents 
                whether a user was at or below the threshold
                value of vists as establish by n * mean_usage.
    '''
    df = low_usage_users(df=df, n=n)
    df = df.groupby(['name']).agg(
        {'user_id':'nunique', 'cohort_size':'first'})[['user_id','cohort_size']]
    df['proportion_low_users'] = df['user_id']/df['cohort_size']
    df = df.sort_values(by='proportion_low_users', ascending=False)
    
    return df