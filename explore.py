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