import pandas as pd
from visualizations import graphs
from misc import helper
import numpy as np

# Import the data from csv to dataframe
minute_data = pd.read_csv('data/minute_measurement_merged.csv')
hourly_data = pd.read_csv('data/hourly_measurement_merged.csv')
daily_data = pd.read_csv('data/daily_measurement_merged.csv')

# Using the help function to replace the id to smaller integers
minute_data = helper.replace_id(minute_data)
hourly_data = helper.replace_id(hourly_data)
daily_data = helper.replace_id(daily_data)


# Group the minute data by id and sum all steps taken
minute_data_grouped = minute_data.groupby(['id'], as_index=False)['steps'].sum()
# Bar chart for total number of steps taken
graphs.bar_chart(minute_data_grouped,
                 x='id',
                 y='steps',
                 x_label='ID',
                 y_label='Total Steps taken for the Duration of Study')


# Group the minute data by id and sum all steps taken
minute_data_grouped = minute_data.groupby(['id'], as_index=False).agg({'mets': 'mean'})
# Bar chart for total number of steps taken
graphs.bar_chart(minute_data_grouped,
                 x='id',
                 y='mets',
                 x_label='ID',
                 y_label='Average METS for the Duration of Study Per Minutes')


# Group the minute data by id and sum all steps taken
minute_data_grouped = minute_data.groupby(['id'], as_index=False).agg({'intensity': 'mean'})
# Bar chart for total number of steps taken
graphs.bar_chart(minute_data_grouped,
                 x='id',
                 y='intensity',
                 x_label='ID',
                 y_label='Average Intensity for the Duration of Study Per Minutes')


# Group the minute data by id and sum all steps taken
minute_data_grouped = minute_data.groupby(['id'], as_index=False).agg({'calories': 'mean'})
# Bar chart for total number of steps taken
graphs.bar_chart(minute_data_grouped,
                 x='id',
                 y='calories',
                 x_label='ID',
                 y_label='Average Calories Consumed for the Duration of Study Per Minutes')


# Group by id for the minute interval data to find the min calories
minute_data_grouped = minute_data.groupby('id')['calories'].transform(lambda x: np.where(x == 0, x.mean(), x))
minute_data_grouped = pd.concat([minute_data['id'], minute_data_grouped], axis=1)
minute_data_grouped = minute_data_grouped.groupby('id', as_index=False).min()
# Plot the minimum calories consumed at rest
graphs.bar_chart(minute_data_grouped,
                 x='id',
                 y='calories',
                 x_label='ID',
                 y_label='Minimum Calories Consumed at Rest for Each Participant')


# Group by id and count the calories consumed per step
minute_data_grouped = minute_data.groupby('id', as_index=False).apply(
    lambda x: pd.Series(
        dict(
            cal_step=sum(x.steps) / sum(x[x.steps > 0].calories))))
# Plot the minimum calories consumed at rest
graphs.bar_chart(minute_data_grouped,
                 x='id',
                 y='cal_step',
                 x_label='ID',
                 y_label='Average Calories Consumed Per Step')


# Split the date_time column into date and time
minute_data[['date', 'time']] = minute_data['date_time'].str.split(' ', 1, expand=True)
minute_data['time'] = pd.to_timedelta(minute_data['time'])


# Count the total amount of time
minute_time = minute_data.groupby(['id'], as_index=False)['time'].count()
minute_time['time'] = minute_time['time']/60


# Group by id and count the calories consumed per step
minute_data_grouped = minute_data.groupby('id', as_index=False).apply(
    lambda x: pd.Series(
        dict(
            no_activity=sum((x.intensity == 0) & (x.mets == 10)))))


minute_data_grouped['no_activity'] = minute_data_grouped['no_activity']/(60*minute_time['time'])
# Plot the minimum calories consumed at rest
graphs.bar_chart(minute_data_grouped,
                 x='id',
                 y='no_activity',
                 x_label='ID',
                 y_label='Percentage of Time Spent with No Physical Activity')


"""
# Plot Total fitbit Time used
graphsbar_chart(minute_time, x='id', y='time', x_label='ID', y_label='Fitbit Time Use During Survey Period (Hours)')

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


