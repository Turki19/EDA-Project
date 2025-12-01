import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Plot Style
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (8, 5)

print('Done')

# The entire database of all cyber attacks published on the news from 2014 to 2025
entire_df = pd.read_excel('Cyber_Events_Database_2014_Oct_2025.xlsx')
entire_df.head()

# A subset of the data that only includes attacks agianst the United States 
# This is chosen for this project because it contains the largest amount of data, and can be easily be analysed for trands 
us_df = entire_df[entire_df['country'] == 'United States of America']
us_df.head()

# Data Exploration
# The current dataset contais 44 features 
us_df.info()

# Removing irrelevant features and features that are mostly Non values
# 11 features selected for this EDA project 
relevant_features = [
    'event_date','year','actor','actor_type',
    'organization','industry','motive','event_type',
    'country','actor_country','state'
    ]

df = us_df[relevant_features].copy()
df.head()

# Check of any missing values, data type of each feature, and the number of entry points
df.info()

# Check for duplicate rows
df.duplicated().sum()

# Removing Duplicates
df.drop_duplicates(inplace=True)

# Check for duplicate rows again
df.duplicated().sum()

# Check for missing values
df.isna().sum()

# Statistical Overview of all categorical features in the dataset
df.describe(include='object')

# The Number of attacks each year, we can see the number of attacks has been increasing each year
df['year'].value_counts()

# The number of attacks aginst each industry, Health care and social assistance received the majority of attacks
df['industry'] = df['industry'].str.title()
df['industry'].value_counts()

# Some Industry names are so long, create abbreviations to each one of them
# Remove industries targted by a very low cyber attacks
rename_map = {
    
    'Professional, Scientific, And Technical Services':'Tech/Science',
    'Administrative And Support And Waste Management And Remediation Services':'Admin/Support',
    'Mining, Quarrying, And Oil And Gas Extraction':'Oil and Gas',
    'Health Care And Social Assistance':'Health Care',
    'Other Services (Except Public Administration)':'Other Services',
    'Real Estate And Rental And Leasing':'Real Estate',
    'Arts, Entertainment, And Recreation':'Entertainment',
    'Accommodation And Food Services':'Accommodation',
    'Transportation And Warehousing':'Transportation',
}
industries_to_drop = ['Agriculture, Forestry, Fishing And Hunting', 'Management Of Companies And Enterprises']
df = df[~df['industry'].isin(industries_to_drop)]
df['industry'] = df['industry'].replace(rename_map)
df['industry'].value_counts()

# The distribution of attacks based on motive
df['motive'].value_counts()

# Remove rara classes based on motive
motives_to_drop = ['Political-espionage','Reputation','Protest,Political-Espionage']
df = df[~df['motive'].isin(motives_to_drop)]
df['motive'].value_counts()

# Which actor type was responsible for most attacks?
df['actor_type'].value_counts()

# Two occurrances of Nation-state becuase of spelling errors
# To resolve the issue capitalize first letter of each word 
df['actor_type'] = df['actor_type'].str.title()
df['actor_type'].value_counts()

# Remove Rare Classes
# There is a very low number of attacks attributed to the terrorist group. Delete them to foucs our analysis on other groups.
actors_to_drop = ['Terrorist']
df = df[~df['actor_type'].isin(actors_to_drop)]
df['actor_type'].value_counts()

# Attacking approach 
df['event_type'] = df['event_type'].str.strip()
df['event_type'].value_counts()

# Use countplot to answer this question, Horizontal overview 
# y-axis industry names, x-axis number of attacks
sns.countplot(data=df, y='industry', order=df['industry'].value_counts().index)
plt.title('Number of Cyber Attacks on each Industry', fontsize=14)
plt.xlabel('Number of Attacks')
plt.ylabel('Industry')
plt.show()

# Create a frequncy table that count how many times each actor type hit each industry. 
# The best way of doing this is by using Cross Tabulation from pandas library
heatmap_data = pd.crosstab(df['actor_type'], df['industry'])

# Plot the Heatmap
plt.figure(figsize=(12, 8)) # adjust figure size
sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='Reds', linewidths=.5) # fmt='d' to round decimal numbers to int
plt.title('Actor Type vs. Target Industry', fontsize=14)
plt.ylabel('Actor Type')
plt.xlabel('Industry')
plt.show()

# Count attacks by Year and Motive
# Group by Year and Motive, then count the rows (size)
motive_year_data = df.groupby(['year', 'motive']).size().reset_index(name='counts')

# Use lindplot to answer this question
sns.lineplot(data=motive_year_data, x='year', y='counts', hue='motive', marker='o')

plt.title('The Yearly Number of Attacks Based on Motives', fontsize=16)
plt.ylabel('Number of Attacks')
plt.xlabel('Year')
plt.legend(title='Motive', loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Use countplot figure to answer this question with hue parameter to split bars

sns.countplot(data=df, y='actor_type', hue='event_type',
             order=df['actor_type'].value_counts().index)

plt.title('Actor Type vs. Event Type', fontsize=16)
plt.xlabel('Number of Attacks')
plt.ylabel('Actor Type')
plt.legend(title='Event Type')
plt.show()

# Count the number of events for each year
# .value_counts() counts them, .sort_index() ensures years are in order (2005, 2006, etc.)
attacks_per_year = df['year'].value_counts().sort_index()

# Use Line Chart figure to answer this question 
sns.lineplot(x=attacks_per_year.index, y=attacks_per_year.values, marker='o')

# Add labels and title
plt.title('Number of Reported Attacks Over the Years (2014-2024)', fontsize=16)
plt.xlabel('Year')
plt.ylabel('Number of Reported Attacks')
plt.show()

# We count the values
actor_counts = df['actor_type'].value_counts()

# Use Bar Chart
sns.barplot(x=actor_counts.values, y=actor_counts.index)

plt.title('Number of Recorded Attacks per each Actor Type', fontsize=16)
plt.xlabel('Number of Recorded Attacks')
plt.ylabel('Actor Type') 
plt.show()

# Group by Year and Actor Type to count attacks per year for each group
actor_trends = df.groupby(['year', 'actor_type']).size().reset_index(name='count')

# Use line chart to answer this question 
sns.lineplot(data=actor_trends, x='year', y='count', hue='actor_type', marker='o')

plt.title('Timeline of Attacks Based on Actor Type', fontsize=16)
plt.ylabel('Number of Attacks')
plt.xlabel('Year')
plt.legend(title='Actor Type', loc='upper left')
plt.grid(True)
plt.show()
