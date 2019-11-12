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