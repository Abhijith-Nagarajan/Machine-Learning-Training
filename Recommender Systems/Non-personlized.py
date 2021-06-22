# Sample of tasks or non-personalized recommder systems
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv(r'./Assignment 1/HW1-data.csv')
df.head()

df.describe()
df.info()

g = sns.barplot(x = df.isnull().sum().index,y = df.isnull().sum().sort_values(ascending=False),palette='viridis')
g.fig.set_size_inches(10,10)

df.isnull().sum().sort_values(ascending=False)

# Task 1
df.mean().sort_values(ascending=False)

# Task 2
df.iloc[:,2:].count().sort_values(ascending=False)

df['1: Toy Story (1995)'].mean()

# Task 3
ratings_over_4 = {}
for col in df.columns:
    if col != 'User' and col != 'Gender (1 =F, 0=M)':
        movie_count = df[col].value_counts()
        ratings_over_4[col] = (sum(movie_count.loc[movie_count.index>=4.0])/(df[col].count()))*100
    
ratings_of_4 = [(key,value) for (key,value) in reversed(sorted(ratings_over_4.items(),key=lambda x:x[1]))]
ratings_of_4  

# Task 4
columns = [col for col in df.columns if col!='1: Toy Story (1995)' and col!='User' and col!='Gender (1 =F, 0=M)']

toy_story_associations = {}
for col in columns:
    index = df.columns.get_loc(col)
    count = 0
    for _,row in df.iterrows():
        if pd.notnull(row[index]) and pd.notnull(row['1: Toy Story (1995)']):
            count+=1
    toy_story_associations[col] = count/17

[print (key,value) for key,value in toy_story_associations.items()]
          
    

# Task 5 
df.corr('pearson')['1: Toy Story (1995)'].sort_values(ascending=False)

#Task 6
df_male_rating = df[df['Gender (1 =F, 0=M)']==0]
df_male_rating = df_male_rating.drop(['User','Gender (1 =F, 0=M)'],axis=1)
df_male_rating.mean()

df_female_rating = df[df['Gender (1 =F, 0=M)']==1]
df_female_rating = df_female_rating.drop(['User','Gender (1 =F, 0=M)'],axis=1)
df_female_rating.mean()

difference_in_ratings = (df_male_rating.mean()-df_female_rating.mean()).sort_values(ascending=False)
difference_in_ratings

print(f"Average male ratings-Average female ratings:{df_male_rating.mean().mean()-df_female_rating.mean().mean()}")

avg_difference_in_ratings = df_female_rating.mean().mean() - df_male_rating.mean().mean()
avg_difference_in_ratings

# Task 7
male_ratings_over_4 = {}
for col in df_male_rating.columns:
     male_movie_count = df_male_rating[col].value_counts()
     male_ratings_over_4[col] = (sum(male_movie_count.loc[male_movie_count.index>=4.0])/(df_male_rating[col].count()))*100

male_ratings_of_4 = pd.Series([value for value in male_ratings_over_4.values()],index=[key for key in male_ratings_over_4.keys()])
male_ratings_of_4

female_ratings_over_4 = {}
for col in df_male_rating.columns:
     female_movie_count = df_female_rating[col].value_counts()
     female_ratings_over_4[col] = (sum(female_movie_count.loc[female_movie_count.index>=4.0])/(df_female_rating[col].count()))*100

female_ratings_of_4 = pd.Series([value for value in female_ratings_over_4.values()],index=[key for key in female_ratings_over_4.keys()])
female_ratings_of_4

difference_in_ratings_over_4 = (male_ratings_of_4 - female_ratings_of_4).sort_values(ascending=False)
difference_in_ratings_over_4
