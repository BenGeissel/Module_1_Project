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
    
 