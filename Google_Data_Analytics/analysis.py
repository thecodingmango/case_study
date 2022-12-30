# Loading the required libraries
import numpy as np
import pandas as pd
from linear_regression.lm_model import *
from visualizations.data_visualizations import *
from datetime import datetime, timedelta


# Import the data from csv to dataframe
minute_data = pd.read_csv('data/minute_measurement_merged.csv')
hourly_data = pd.read_csv('data/hourly_measurement_merged.csv')
daily_data = pd.read_csv('data/daily_measurement_merged.csv')

# Replace the id of dataframe to a range from 1:33
id_index = dict(zip(minute_data['id'].unique(), np.arange(1, 34)))

# For every row in id
for ids in minute_data['id'].unique():

    # Replace the id with small index numbers from 1-33
    minute_data['id'] = minute_data['id'].replace(ids, id_index[ids])
    hourly_data['id'] = hourly_data['id'].replace(ids, id_index[ids])
    daily_data['id'] = daily_data['id'].replace(ids, id_index[ids])

# Generate summary statistic of our data
minute_data.iloc[:, 1:].describe()
hourly_data.iloc[:, 1:].describe()
daily_data.iloc[:, 1:].describe()

# Group the measurements by each participant
minute_data.groupby('id', as_index=False).agg({'steps': 'mean', 'mets': 'mean', 'intensity': 'mean', 'calories': 'mean'})
hourly_data.groupby('id', as_index=False).agg({'hourly_steps': 'mean', 'avg_hourly_mets': 'mean', 'avg_hourly_intensity': 'mean', 'hourly_calories_burned': 'mean'})
daily_data.groupby('id', as_index=False).agg({'daily_steps': 'mean', 'avg_daily_mets': 'mean', 'avg_daily_intensity': 'mean', 'daily_calories_burned': 'mean'})

# Create a response and explanatory variable
response = hourly_data['hourly_calories_burned']
explanatory = hourly_data.iloc[:, [2, 3, 4]]

# Create a linear regression model using grouped hourly data
lm_hourly = lm_model(response, explanatory)
lm_hourly.summary()

# Ridge regression
lm_reg = lm_regularized(response, explanatory, l1=0, alpha=5)
lm_reg.summary()

# Plot the correlation of the hourly data
hourly_corr = hourly_data.iloc[:, 2:].corr()
plot_corr(hourly_corr)

# Check the VIF values from the regression model for hourly data
vif_lm_hourly = vif(lm_hourly)
vif_lm_hourly

# ---------------------------------------------------------------------------------------------------------------------

# Data visualization section

# Group the minute data by id and sum all steps taken
minute_data_grouped = minute_data.groupby(['id'], as_index=False)['steps'].sum()
# Bar chart for total number of steps taken
bar_chart(minute_data_grouped, x='id', y='steps', x_label='ID', y_label='Total Steps taken for the Duration of Study')

# Group the minute data by id and sum all steps taken
minute_data_grouped = minute_data.groupby(['id'], as_index=False).agg({'mets': 'mean'})
# Bar chart for total number of steps taken
bar_chart(minute_data_grouped, x='id', y='mets', x_label='ID', y_label='Average METS for the Duration of Study Per Minutes')

# Group the minute data by id and sum all steps taken
minute_data_grouped = minute_data.groupby(['id'], as_index=False).agg({'intensity': 'mean'})
# Bar chart for total number of steps taken
bar_chart(minute_data_grouped, x='id', y='intensity', x_label='ID', y_label='Average Intensity for the Duration of Study Per Minutes')

# Group the minute data by id and sum all steps taken
minute_data_grouped = minute_data.groupby(['id'], as_index=False).agg({'calories': 'mean'})
# Bar chart for total number of steps taken
bar_chart(minute_data_grouped, x='id', y='calories', x_label='ID', y_label='Average Calories Consumed for the Duration of Study Per Minutes')

# Group by id for the minute interval data to find the min calories
minute_data_grouped = minute_data.groupby('id')['calories'].transform(lambda x: np.where(x == 0, x.mean(), x))
minute_data_grouped = pd.concat([minute_data['id'], minute_data_grouped], axis=1)
minute_data_grouped = minute_data_grouped.groupby('id', as_index=False).min()
# Plot the minimum calories consumed at rest
bar_chart(minute_data_grouped, x='id', y='calories', x_label='ID', y_label='Minimum Calories Consumed at Rest for Each Participant')

# Group by id and count the calories consumed per step
minute_data_grouped = minute_data.groupby('id', as_index=False).apply(lambda x: pd.Series(dict(
    cal_step=sum(x.steps) / sum(x[x.steps > 0].calories))))
# Plot the minimum calories consumed at rest
bar_chart(minute_data_grouped, x='id', y='cal_step', x_label='ID', y_label='Average Calories Consumed Per Step')

# Split the date_time column into date and time
minute_data[['date', 'time']] = minute_data['date_time'].str.split(' ', 1, expand=True)
minute_data['time'] = pd.to_timedelta(minute_data['time'])

# Count the total amount of time
minute_time = minute_data.groupby(['id'], as_index=False)['time'].count()
minute_time['time'] = minute_time['time']/60

# Group by id and count the calories consumed per step
minute_data_grouped = minute_data.groupby('id', as_index=False).apply(lambda x: pd.Series(dict(
    no_activity=sum((x.intensity == 0) & (x.mets == 10)))))

minute_data_grouped['no_activity'] = minute_data_grouped['no_activity']/(60*minute_time['time'])
# Plot the minimum calories consumed at rest
bar_chart(minute_data_grouped, x='id', y='no_activity', x_label='ID',
          y_label='Percentage of Time Spent with No Physical Activity')








# Plot Total fitbit Time used
bar_chart(minute_time, x='id', y='time', x_label='ID', y_label='Fitbit Time Use During Survey Period (Hours)')





# Split the time_stamp into date and time column
hourly_data[['date', 'time']] = hourly_data['time_stamp'].str.split(' ', 1, expand=True)
hourly_data['time'] = pd.to_timedelta(hourly_data['time'])

# Group the hourly data and count how many hours each user was active
hourly_time = hourly_data.groupby('id', as_index=False)['time'].count()

# Find the mean use time of the fitbit users
hourly_time['time'] = hourly_time['time']/(30.625)

# Plot the average time use per day
bar_chart(hourly_time, x='id', y='time', x_label='ID', y_label='Average Fitbit Time Use During Survey Period (Hours)')

max(pd.to_datetime(hourly_data['time_stamp']))






"""
date = pd.to_datetime(hourly_data['time_stamp'], format='%Y-%m-%d %H:00:00')
date = [datetime.datetime.weekday(i) for i in date]
date
"""
