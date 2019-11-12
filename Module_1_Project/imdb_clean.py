# Import necessary libraries with aliases
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv

def merge_imdb_files():
    '''Function to merge necessary IMDB tables
    
    Input: DataFrames with imdb information including 'nconst' and 'tconst' features to be used as keys
    
    Output: Complete DataFrame with corresponding keys
    
    '''

