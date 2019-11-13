# Import necessary libraries with aliases
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv

def merge_clean_imdb_files():
    '''Function to merge necessary IMDB tables
    
    Input: DataFrames with imdb information including 'nconst' and 'tconst' features to be used as keys
    
    Output: None. DataFrame is now changed and clean.
    
    '''
    # Read in IMDB files
    imdb_name_basics = pd.read_csv('imdb.name.basics.csv')
    imdb_title_basics = pd.read_csv('imdb.title.basics.csv')
    imdb_title_crew = pd.read_csv('imdb.title.crew.csv')
    imdb_title_principals = pd.read_csv('imdb.title.principals.csv')
    imdb_title_ratings = pd.read_csv('imdb.title.ratings.csv')
    
    #Merge IMDB files into common DataFrame using pandas
    imdb_title_ratings_principals = pd.merge(imdb_title_ratings, imdb_title_principals, on = 'tconst', how = 'outer')
    imdb_title_full = pd.merge(imdb_title_ratings_principals, imdb_title_crew, on = 'tconst', how = 'outer')
    imdb_title_names_full = pd.merge(imdb_title_full, imdb_name_basics, on = 'nconst', how = 'outer')
    
    #Drop all columns which are not primary_name, category, averagerating, or primary_profession
    imdb_title_names_full = imdb_title_names_full.drop([
        'job', 
        'birth_year',
        'death_year',
        'ordering',
        'nconst',
        'numvotes',
        'directors',
        'writers',
        'characters',
        'known_for_titles',
        'tconst'],
        axis = 1)
    
    #Remove instances where primary_name has no averagerating given
    imdb_clean = imdb_title_names_full.dropna()
    
    return imdb_clean
    

def movie_count_dist(dataframe):
    '''
    Function to filter primary names by movie counts 10 or greater.
    
    Input: Cleaned and merged IMDB dataframe
    
    Output: Plot of movie count distribution
    '''
    
    imdb_names_count = dataframe.primary_name.value_counts()
    imdb_prominent_names = imdb_names_count.loc[imdb_names_count > 9]
    fig = plt.figure()
    imdb_graph = sns.distplot(imdb_prominent_names)
    plt.title('Movie Counts by Name')
    plt.ylabel('Percentage of Distribution')
    plt.xlabel('Number of Movies')
    plt.show()
    
    return None


def highest_rated_personnel(dataframe):
    '''
    Function to sort personnel by overall average movie rating regardless of job category.
    
    Input: IMDB dataframe with movie appearance >= 10
    
    Output: Data table sorted by average movie rating. Displays top 10 personnel
    '''
    
    name, count = np.unique(dataframe.primary_name, return_counts=True)

    more_than_9 = []

    for name, count in zip(name, count):
        if count > 9:
            more_than_9.append(name)
        
    top_name_ratings = dataframe[dataframe.primary_name.isin(more_than_9)].sort_values('averagerating',
                                                                                                 ascending = False).iloc[0:10]
    top_name_ratings.drop('primary_profession', axis = 1, inplace = True)
    top_name_ratings.style.set_properties(**{'text_align': 'center'})
    top_name_ratings.rename(columns = {'averagerating':'Average Rating', 'category': 'Category',
                                       'primary_name':'Primary Name'}, inplace = True)
    
    return top_name_ratings


def top_ratings_by_category(dataframe):
    '''
    Function to sort highest rated personnel by job category
    
    Input: Data table sorted by highest movie rating regardless of job category
    
    Output: Data table with highest movie rating personnel for each job category
    '''
    
    top_category_ratings = dataframe.groupby(['Category']).max()
    
    return top_category_ratings.style.set_properties(**{'text_align':'center'})