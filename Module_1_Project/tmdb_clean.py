# Import libraries with proper aliases
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv

# Create function to fix numerical data; Budget and Gross have '$' and ','; Change to integer
def budget_gross_number_fix(dataframe, column):
    '''
    Function to fix the format of money values in the dataframe. Removes '$' and ',' and changes to integer type
    
    Input: Dataframe and Column that has data in this format
    
    Output: None. Data in dataframe is changed
    '''
    
    dataframe[column] = dataframe[column].apply(lambda x: x.replace('$', ''))
    dataframe[column] = dataframe[column].apply(lambda x: x.replace(',', ''))
    dataframe[column] = dataframe[column].astype('int')
    return None

def clean(file):
    '''
    Function to clean the TMDB Budgets Data CSV File.
    
    Input: CSV File name as string
    
    Output: Cleaned DataFrame
    '''
    
    # Read in the TMDB Budgets Data
    tmdb_budgets_df = pd.read_csv(file)
    
    # Combine Movie and Release Date to account for remakes or movies with same name
    tmdb_budgets_df['movie_date'] = tmdb_budgets_df.movie + ' ' + tmdb_budgets_df.release_date
    
    # Apply budget_gross_number_fix function to the three necessary columns
    budget_gross_number_fix(tmdb_budgets_df, 'production_budget')
    budget_gross_number_fix(tmdb_budgets_df, 'domestic_gross')
    budget_gross_number_fix(tmdb_budgets_df, 'worldwide_gross')
    
    # Create column for binned budgets
    tmdb_budgets_df['binned_budget'] = pd.cut(x=tmdb_budgets_df['production_budget'],
                                              bins= [0, 500000, 1000000, 5000000, 10000000, 25000000,
                                                     50000000, 100000000, 500000000])
    
    # Data Assumption: Only movies that actually go to the box office. Not straight to Netflix or DVD because of 0 gross value.
    # Filter out movies with 0 gross domestic or worldwide
    tmdb_budgets_df = tmdb_budgets_df[tmdb_budgets_df.domestic_gross != 0]
    tmdb_budgets_df = tmdb_budgets_df[tmdb_budgets_df.worldwide_gross != 0]
    
    return tmdb_budgets_df