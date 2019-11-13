# Import libraries with proper aliases
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv

def clean(file):
    '''
    Function to clean the BOM Data CSV File.
    
    Input: CSV File name as string
    
    Output: Cleaned DataFrame
    '''
    
    # Read in the BOM Data
    bom_df = pd.read_csv(file)
    
    # Data Assumption: Only movies that actually go to the box office. Not straight to Netflix or DVD because of 0 gross value.
    # Filter out movies with 0 Gross Domestic
    bom_df = bom_df[bom_df.domestic_gross != 0]
    
    # Fix Foreign Gross N/A values
    # Assume 0 if is N/A
    bom_df.foreign_gross.fillna(value = 0, inplace = True)
    
    # Convert to string type
    bom_df.foreign_gross = bom_df.foreign_gross.astype('str')
    
    # Remove commas from number type
    bom_df.foreign_gross = bom_df.foreign_gross.apply(lambda x: x.replace(',', ''))
    
    # Convert to float type
    bom_df.foreign_gross = bom_df.foreign_gross.astype('float64')
    
    # Drop remaining N/A values as it is a very small portion of the dataset
    bom_df.dropna(inplace = True)
    
    return bom_df


def bom_group_and_sort(dataframe):
    '''
    Function to group and sort studio data from Box Office Mojo. Groups by studio and aggregates
    the mean domestic gross revenue. Sorts and slices the top 10 studios by average.
    
    Input: Cleaned BOM dataframe
    
    Output: Grouped and Sorted Top 10 Dataframe
    '''
    
    bom_studio_grouped_df = dataframe.groupby(by = 'studio', axis = 0).mean()
    
    bom_studio_grouped_topten_df = bom_studio_grouped_df.sort_values('domestic_gross',
                                                                 ascending = False)[:10]['domestic_gross']
    
    return bom_studio_grouped_topten_df


def plot_studios(dataframe):
    '''
    Function to plot top 10 studios by average gross domestic revenue.
    
    Input: Grouped and Sorted data frame
    
    Output: Plot of top 10 studios by average gross domestic revenue
    '''
    
    fig = plt.figure(figsize = (10,10), facecolor = 'w')
    ax = fig.add_subplot(1,1,1)
    ax.set_facecolor('lightgray')
    dataframe.plot(kind = 'bar', color = 'darkblue');
    plt.xlabel('Studio', fontsize = 15)
    plt.ylabel("Mean Domestic Gross in 100,000,000's", fontsize = 15)
    plt.title('Top 10 Mean Domestic Gross by Studio', fontsize = 20)
    plt.show()
    
    return None