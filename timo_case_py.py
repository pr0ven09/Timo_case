# -*- coding: utf-8 -*-
"""Timo case Full

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14KnD3H4L7fJG0Clqd1kDny4PCjw1J7KC

# **Table of Contents**
##**Timo test_case_Bao Cuong NG**
1. Overview
2. Prepare the data
3. EDA and visualization

# **1. Overview**

##**Business understanding**

This dataset contains Timo Superbank users' data including personal information (info) and transaction records. Regarding this, the stakeholders want to acknowledge the business landscape and next steps for improvement.

##**Dataset background**

The dataset includes several attributes regarding users' info:

1.   User ID: account_id
2.   User DOB: date_of_birth
3.   Transaction date & time: txn_ts
4.   Transaction value: txn_amount
5.   Transaction type: txn_type_code

Based on the info provided, a concept for an in-depth analysis is generated:

**General info overview -> Demographic analysis -> Transaction analysis -> Conclusion & What's next?**

# **2. Prepare the data**
**Importing libs**
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pointbiserialr
import warnings
import plotly.express as px
from plotly.offline import iplot
from google.colab import data_table
from vega_datasets import data

"""**Importing dataset**

*The dataset has already been pre-processed and cleaned in excel for data manipulation convenience (removed duplicate, adding up columns...)*
"""

file_path = 'https://drive.google.com/uc?id=1N1kXWKC-W0FVQ6XEASuSo6SkJDgbCo1H'
df = pd.read_csv((file_path),sep = ';')
print(df.head())

print("\nBasic Information about the Dataset:")
print(df.info())

#Unique value of each column
print(df.nunique())

"""#**3. EDA and Visualization**

##**General information**

Calculating the users' balance (Assuming every account were having a 0 value balance before the record)
"""

user_balance = df.groupby('account_id')['txn_amount'].sum().reset_index(name='balance')
print(user_balance)

#Total balance & avg balance
user_balance['balance'].mean()

user_balance['balance'].sum()

"""Calculate age and divide in to groups"""

current_year = pd.Timestamp.now().year
user_df['age'] = current_year - pd.to_datetime(user_df['date_of_birth']).dt.year

print(user_df['age'])

df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels)

unique_users_age_group_counts = df.drop_duplicates('account_id').groupby('age_group')['account_id'].count()

print(unique_users_age_group_counts)

"""General statistics"""

df.describe()

"""##**Demographic**
Age distribution

"""

unique_users_df = df.drop_duplicates(subset='account_id')

# Histogram plot
plt.figure(figsize=(10, 6))
plt.hist(unique_users_df['age'], bins=20, color='skyblue', edgecolor='black', alpha=0.7)
plt.title('Age Distribution')
plt.xlabel('Age')
plt.ylabel('User count')
plt.grid(True)
plt.show()

unique_users_df['age'].describe()

"""Total transaction value by age **groups**"""

age_group_balance = df.groupby('age_group')['txn_abs'].sum().reset_index(name='sum_balance_by_age_group')
df.groupby('age_group')['txn_abs'].sum().reset_index(name='sum_balance_by_age_group')

"""Transaction count"""

df.groupby('age_group')['txn_amount'].count().reset_index(name='transaction_count')
total_transaction_count = df['txn_amount'].count()
total_df = pd.DataFrame({'age_group': ['Total'], 'transaction_count': [total_transaction_count]})
pd.concat([transaction_count_by_age_group, total_df], ignore_index=True)

"""Average transaction value"""

data_table.enable_dataframe_formatter()
age_group_balance['average_transaction_value'] = (age_group_balance['sum_balance_by_age_group'] / transaction_count_by_age_group['transaction_count'])
data_table.DataTable(age_group_balance)

"""## **Transaction**
Trends in Q1/2021
"""

transaction_value_by_month_and_type = df.groupby(['month', 'txn_type_code'])['txn_abs'].sum().reset_index()
pivot_table = transaction_value_by_month_and_type.pivot(index='month', columns='txn_type_code', values='txn_abs')

# Plotting
plt.figure(figsize=(10, 6))
for column in pivot_table.columns:
    plt.plot(pivot_table.index, pivot_table[column], marker='o', label=column)

plt.xlabel('Month')
plt.ylabel('Total Transaction Value')
plt.title('Transaction Value by Month and Type (Unit)')
plt.xticks(pivot_table.index)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

"""Average transaction value by type"""

avg_transaction_by_type = df.groupby('txn_type_code')['txn_abs'].mean().reset_index()
avg_transaction_by_type.columns = ['Transaction Type', 'Average Transaction Value']
display(data_table.DataTable(avg_transaction_by_type))

"""Correlation check between transaction value & daytime/age/date


"""

correlation = df['age'].corr(df['txn_abs'])
print("Correlation between age and transaction value:", correlation)

df['txn_ts_time'] = pd.to_numeric(df['txn_ts_time'], errors='coerce')
correlation = df['txn_abs'].corr(df['txn_ts_time'])
print("Correlation between transaction amount and hour of the day:", correlation)

df['txn_ts_numeric'] = df['txn_ts'].astype(int)
correlation = df['txn_ts_numeric'].corr(df['txn_abs'])
print("Correlation between date and transaction value:", correlation)

"""Distribution of transaction during a day time & week"""

#Change data type
df.loc[0, 'txn_ts'] = "2021-01-01 11:52:00"
df['txn_ts'] = pd.to_datetime(df['txn_ts'], format='%Y-%m-%d %H:%M:%S')
df['txn_ts_numeric'] = df['txn_ts'].dt.strftime('%Y%m%d%H%M%S')
df['txn_ts_numeric'] = df['txn_ts'].astype(int)

df['hour_of_day'] = df['txn_ts'].dt.hour
df['day_of_week'] = df['txn_ts'].dt.day_name()

weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
transaction_count_by_day_hour = df.pivot_table(index='hour_of_day', columns='day_of_week', aggfunc='size', fill_value=0)
transaction_count_by_day_hour = transaction_count_by_day_hour.reindex(columns=weekday_order)

# Plotting the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(transaction_count_by_day_hour, cmap='YlGnBu', linewidths=0.5)
plt.title('Distribution of Transactions by Hour of the Day and Day of the Week')
plt.xlabel('Day of the Week')
plt.ylabel('Hour of the Day')
plt.yticks(rotation=0)
plt.show()

"""**What's next?**

The analysis of the above results is included in the presentation (Link)

In case of any concern, please contact me via my email - cuongnguyen1212122@gmail.com; or personal phone - +84-965-962-762
"""