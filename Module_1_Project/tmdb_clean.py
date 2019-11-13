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

def plot_budget_sizes(dataframe):
    '''
    Function to plot the budget distribution in order to determine budget binning
    
    Input: Cleaned dataframe
    
    Output: Plot of budget distribution.
    '''
    
    fig = plt.figure(figsize = (8,5))
    sns.distplot(dataframe.production_budget, bins = 50, color = 'darkred', kde = True);
    plt.xlabel("Budget in 100,000,000's")
    plt.ylabel('% of Movies Produced')
    plt.title('Budget Spread', fontsize = 20)
    plt.show()
    return None

# Define bin labels in easy to read format
bins_labels = ['($0, $500K]', '($500K, $1M]', '($1M, $5M]',
               '($5M, $10M]', '($10M, $25M]', '($25M, $50M]',
               '($50M, $100M]', '($100M, $500M]']

def domestic_ROI(dataframe):
    '''
    Function to calculate domestic ROI from TMDB data. Pivots the data and creates a dictionary used for plotting.
    
    Input: Cleaned dataframe
    
    Output: Dictionary with label keys and domestic ROI values for plotting.
    '''
    
    dataframe['Gross_ROI'] = ((dataframe.domestic_gross - dataframe.production_budget) / 
                              dataframe.production_budget)
    
    tmdb_budgets_domestic_pivot_df = pd.pivot_table(dataframe, index = 'movie_date',
                                                    columns = 'binned_budget',
                                                    values = 'Gross_ROI',
                                                    aggfunc = 'sum')
    
    domestic_roi_by_budget = tmdb_budgets_domestic_pivot_df.mean()

    domestic_roi_dict = {}
    for label in tmdb_budgets_domestic_pivot_df.columns:
        domestic_roi_dict[str(label)] = domestic_roi_by_budget[label]
    domestic_roi_dict = dict(zip(bins_labels, list(domestic_roi_dict.values())))
    
    return domestic_roi_dict
    
    
def worldwide_ROI(dataframe):
    '''
    Function to calculate worldwide ROI from TMDB data. Pivots the data and creates a dictionary used for plotting.
    
    Input: Cleaned dataframe
    
    Output: Dictionary with label keys and worldwide ROI values for plotting.
    '''

    dataframe['Worldwide_ROI'] = ((dataframe.worldwide_gross - dataframe.production_budget) / 
                                  dataframe.production_budget)
    
    tmdb_budgets_worldwide_pivot_df = pd.pivot_table(dataframe, index = 'movie_date',
                                                    columns = 'binned_budget',
                                                    values = 'Worldwide_ROI',
                                                    aggfunc = 'sum')
    
    worldwide_roi_by_budget = tmdb_budgets_worldwide_pivot_df.mean()
    
    worldwide_roi_dict = {}
    for label in tmdb_budgets_worldwide_pivot_df.columns:
        worldwide_roi_dict[str(label)] = worldwide_roi_by_budget[label]
    worldwide_roi_dict = dict(zip(bins_labels, list(worldwide_roi_dict.values())))
    
    return worldwide_roi_dict

def plot_ROI(domestic_dict, worldwide_dict):
    '''
    Function to plot domestic and worldwide ROI by budget bins.
    
    Input: Domestic and worldwide plotting dictionaries from domestic_ROI and worldwide_ROI functions.
    
    Output: Plot of domestic and worldwide ROI by budget bins
    '''
    
    fig = plt.figure(figsize=(20, 10))
    X = np.arange(len(domestic_dict))
    ax = plt.subplot(111)
    ax.set_facecolor('lightgray')
    ax.bar(X, domestic_dict.values(), width=0.3, color='darkblue')
    ax.bar(X+0.3, worldwide_dict.values(), width=0.3, color='blue', alpha = .7)
    ax.legend(('Domestic','Worldwide'), fontsize = 20)
    plt.xticks(X, domestic_dict.keys(), fontsize = 12)
    plt.title("ROI by Budget", fontsize=40)
    plt.ylabel('ROI', fontsize = 25)
    plt.xlabel('Budget', fontsize = 25)
    plt.tight_layout()
    plt.show()
    
    return None