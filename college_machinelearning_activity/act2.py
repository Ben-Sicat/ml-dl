# -*- coding: utf-8 -*-
"""
Created on Thu May 16 15:28:02 2024

@author: cer_ben
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msn
# import datetime as dt
# import os
# import sys

df = pd.read_csv('https://github.com/adelnehme/python-for-spreadsheet-users-webinar/blob/master/datasets/airbnb.csv?raw=true', index_col = 'Unnamed: 0')
# =============================================================================
# PART1
# =============================================================================
df['coordinates'] =df['coordinates'].str.replace('(','')
df['coordinates'] =df['coordinates'].str.replace(')','')

lat_long = df['coordinates'].str.split(',', expand = True)

df['longitude'] = lat_long[1]
df['latitude'] = lat_long[0]

df['latitude']=df['latitude'].astype('float')
df['longitude']=df['longitude'].astype('float')

df.drop('coordinates',axis=1,inplace=True)
###############
df['room_type']=df['room_type'].str.lower()





########################

df['room_type'] = df['room_type'].str.strip(' room')
df['room_type'] = df['room_type'].str.strip(' ')
#switch
df['room_type'] = df['room_type'].str.replace("entire home/apt","home")

df['room_type'] = df['room_type'].str.replace("home","entire home/apt")

df['room_type'].unique()
# =============================================================================
# TASK 1
# =============================================================================


df['neighbourhood_full'].head()

borough_neighborhood = df['neighbourhood_full'].str.split(", ", expand = True)
df['borough'] = borough_neighborhood[0]
df['neighbourhood'] = borough_neighborhood[1]

df.drop('neighbourhood_full', axis =1, inplace =True)



# =============================================================================
# TASK 2
# =============================================================================


sns.displot(df['rating'], bins=20)
plt.show()


isolated_rating=df[df['rating'] > 5.0]

df.drop(isolated_rating.index,inplace=True)


sns.distplot(df['rating'], bins = 20)
plt.show()


max_rating = df['rating'].max()



# =============================================================================
# TASK 3
# =============================================================================


msn.matrix(df)
plt.show()


msn.matrix(df.sort_values(by = 'rating'))

plt.show()

msn.bar(df)
plt.show()


miss_rating = df[df['rating'].isna()].describe()
miss_num_stay =  df[df['number_of_stays'].isna()].describe()
miss_5_star = df[df['5_stars'].isna()].describe()
miss_reviews_per_month = df[df['reviews_per_month'].isna()].describe()


#impute data from NAN to 0
df = df.fillna({'reviews_per_month': 0,
                'number_of_stays': 0,
                '5_stars': 0,
                'rating': 0})



df['is_rated'] = df['rating'].notna().astype(int)

miss_prices=df[df['price'].isna()].describe()

df['price'] = df['price'].str.strip('$')
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['room_type'] = pd.Categorical(df['room_type'])

sns.boxplot(x = df['room_type'], y = df['price'], data = df)
plt.ylim(0, 400)

plt.xlabel('Room Type')
plt.xticks(rotation=45) 
plt.ylabel('Price')

plt.show()
##########################
median_prices = df.groupby('room_type')['price'].median()

##########################
# =============================================================================
# IMPUTE PRICE
# =============================================================================


def impute_price(df):
  """
  impute missing prices. instead of getting the median, prices should be based
  on listing with similar data

  Parameters
  ----------
  df (pandas.DataFrame):
    DESCRIPTION.

  Returns
  -------
pandas.DataFrame: The DataFrame with imputed prices.
  """

  df_imputed = df.copy()

  for room_type in ['entire home/apt', 'shared', 'private']:
    curr_missing_room = df_imputed.query('price.isna() & room_type == @room_type')

    for index in curr_missing_room.index:
      curr_rating = df_imputed.loc[index, 'rating']

      similar = df_imputed[(df_imputed['room_type'] == room_type) & (np.abs(df_imputed['rating'] - curr_rating) <= 1)]
      if not similar.empty:
        imputed_price = similar['price'].median() 
        df_imputed.loc[index, 'price'] = imputed_price
      else:
        room_type_prices = df_imputed[df_imputed['room_type'] == room_type]['price']
        if not room_type_prices.empty: 
          imputed_price = room_type_prices.median()
          df_imputed.loc[index, 'price'] = imputed_price

  return df_imputed

df = impute_price(df.copy())



df.isna().sum()



















