# Import libraries with proper aliases
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv
%matplotlib inline

# Read in the TMDB Budgets Data
tmdb_budgets_df = pd.read_csv('tn.movie_budgets.csv.gz')

# Combine Movie and Release Date to account for remakes or movies with same name
tmdb_budgets_df['movie_date'] = tmdb_budgets_df.movie + ' ' + tmdb_budgets_df.release_date

# Create function to fix numerical data; Budget and Gross have '$' and ','; Change to integer
def budget_gross_number_fix(series):
    series = series.apply(lambda x: x.replace('$', ''))
    series = series.apply(lambda x: x.replace(',', ''))
    series = astype('int')
    return None

# Apply budget_gross_number_fix function to the three necessary columns
budget_gross_number_fix(tmdb_budgets_df.production_budget)
budget_gross_number_fix(tmdb_budgets_df.domestic_gross)
budget_gross_number_fix(tmdb_budgets_df.worldwide_gross)

# Look at where to make more budget bins with a plot
fig = plt.figure(figsize = (8,5))
sns.distplot(tmdb_budgets_df.production_budget, bins = 50, color = 'r');
plt.xlabel("Budget in 100,000,000's")
plt.ylabel('Distribution Amount')
plt.title('Budget Spread', fontsize = 20)
plt.show()
#Many smaller budgets than large budgets

# Create column for binned budgets
tmdb_budgets_df['binned_budget'] = pd.cut(x=tmdb_budgets_df['production_budget'],
                                          bins= [0, 500000, 1000000, 5000000, 10000000, 25000000,
                                                 50000000, 100000000, 500000000])

# Create columns for Return on Investment for both Domestic and Worldwide
tmdb_budgets_df['Gross_ROI'] = ((tmdb_budgets_df.domestic_gross - tmdb_budgets_df.production_budget) / 
                                tmdb_budgets_df.production_budget)
tmdb_budgets_df['Worldwide_ROI'] = ((tmdb_budgets_df.worldwide_gross - tmdb_budgets_df.production_budget) / 
                                    tmdb_budgets_df.production_budget)

# Data Assumption: Only movies that actually go to the box office. Not straight to Netflix or DVD because they would have 0 gross.
# Filter out movies with 0 gross domestic or worldwide
tmdb_budgets_df = tmdb_budgets_df[tmdb_budgets_df.domestic_gross != 0]
tmdb_budgets_df = tmdb_budgets_df[tmdb_budgets_df.worldwide_gross != 0]

# Create Pivot Tables for both Domestic and Worldwide ROI
tmdb_budgets_domestic_pivot_df = pd.pivot_table(tmdb_budgets_df, index = 'movie_date',
                                              columns = 'binned_budget',
                                              values = 'Gross_ROI',
                                               aggfunc = 'sum')

tmdb_budgets_worldwide_pivot_df = pd.pivot_table(tmdb_budgets_df, index = 'movie_date',
                                              columns = 'binned_budget',
                                              values = 'Worldwide_ROI',
                                               aggfunc = 'sum')

# Create a Series of the mean ROI by binned budget for both domestic and worldwide
domestic_roi_by_budget = tmdb_budgets_domestic_pivot_df.mean()

worldwide_roi_by_budget = tmdb_budgets_worldwide_pivot_df.mean()

# Create an equivalent dictionary to the series generated above. These will be used for plotting.
worldwide_roi_dict = {}
for label in tmdb_budgets_worldwide_pivot_df.columns:
    worldwide_roi_dict[str(label)] = worldwide_roi_by_budget[label]
worldwide_roi_dict

domestic_roi_dict = {}
for label in tmdb_budgets_domestic_pivot_df.columns:
    domestic_roi_dict[str(label)] = domestic_roi_by_budget[label]
domestic_roi_dict

# Create a barplot to show domestic and worldwide ROI compared to Budget Bin
fig = plt.figure(figsize=(20, 10))
X = np.arange(len(domestic_roi_dict))
ax = plt.subplot(111)
ax.bar(X, domestic_roi_dict.values(), width=0.3, color='b')
ax.bar(X+0.3, worldwide_roi_dict.values(), width=0.3, color='g', alpha = .3)
ax.legend(('Domestic','Worldwide'), fontsize = 20)
plt.xticks(X, domestic_roi_dict.keys())
plt.title("ROI by Budget", fontsize=40)
plt.ylabel('ROI', fontsize = 25)
plt.xlabel('Budget', fontsize = 25)
plt.tight_layout()
plt.show()