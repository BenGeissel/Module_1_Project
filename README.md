# **Module 1 Project**

## *Project Members: Ben Geissel & Andrew Cole*

### Goals:
Answer Microsoft's questions regarding the movie industry and how they should invest their money.
- Which studios generate the most gross domestic revenue on average?
- How does budget size affect return on investment?
- Who are the best movie personnel to hire?


### Responsibilities:
#### Ben:
- Work with the financial data from both the Box Office Mojo and The Movie Database datasets to discover monetary success by studio and budget
- Create appropriate visualizations from the financial datasets
- Create cleaning modules for the financial datasets
- Create markdown README file
- Collaborate with Andrew on both technical and non-technical jupyter notebooks
- Present concepts to "Microsoft"
#### Andrew:
- Work with the IMDB dataset to discover which movie personnel (actors, producers, etc...) produce the highest ratings
- Create appropriate visualizations and data tables from the IMDB dataset
- Create cleaning module for the IMDB dataset
- Create slide deck for presentation
- Collaborate with Ben on both technical and non-technical jupyter notebooks
- Present concepts to "Microsoft"


### Summary of Included Files:
The following files are included under the Module_1_Project folder within the Github repository:
- Mod_1_Project_Technical_Audience_AC_BG.ipynb
    - Jupyter Notebook for technical audience
    - PEP 8 Standards
    - Imports cleaning modules
    - Data importation, data cleaning, visualizations and charts
- Mod_1_Project_Non_Technical_Audience_AC_BG.ipynb
    - Jupyter Notebook for non-technical audience
    - Description of analysis purpose
    - Appropriate visualizations and summary tables
    - Actionable insights
- bom_clean.py
   - Cleaning module for the Box Office Mojo Dataset
   - Fix null values
   - Returns cleaned dataframe
   - Additional functions in module for use in Non-Technical JN
- tmdb_clean.py
   - Cleaning module for the The Movie Database budgets dataset
   - Defines a function to deal with numerical values in money style strings with '$' and ',' characters
   - Bins budgets into determined bins
   - Drops movies with 0 gross revenue
   - Returns cleaned dataframe
   - Additional functions in module for use in Non-Technical JN
- imdb_clean.py
    - Cleaning module for the IMDB datasets
    - Merges and cleans IMDB datasets into one dataframe and drops unnecessary features and null entries
    - Returns single cleaned dataframe for all IMDB data
    - Additional functions in module for use in Non-Technical JN
- CSV Data Files
    - Files containing the datasets used in the analysis
