# Loading the required libraries
from linear_regression.lm_model import *
from visualizations.graphs import *
from misc import helper
import pandas as pd

# Import the data from csv to dataframe
minute_data = pd.read_csv('data/minute_measurement_merged.csv')
hourly_data = pd.read_csv('data/hourly_measurement_merged.csv')
daily_data = pd.read_csv('data/daily_measurement_merged.csv')

# Using the help function to replace the id to smaller integers
minute_data = helper.replace_id(minute_data)
hourly_data = helper.replace_id(hourly_data)
daily_data = helper.replace_id(daily_data)


# Generate summary statistic of our data
minute_data.iloc[:, 1:].describe()
hourly_data.iloc[:, 1:].describe()
daily_data.iloc[:, 1:].describe()

# Group the measurements by each participant
minute_data.groupby('id', as_index=False).agg({'steps': 'mean',
                                               'mets': 'mean',
                                               'intensity': 'mean',
                                               'calories': 'mean'})

hourly_data.groupby('id', as_index=False).agg({'hourly_steps': 'mean',
                                               'avg_hourly_mets': 'mean',
                                               'avg_hourly_intensity': 'mean',
                                               'hourly_calories_burned': 'mean'})

daily_data.groupby('id', as_index=False).agg({'daily_steps': 'mean',
                                              'avg_daily_mets': 'mean',
                                              'avg_daily_intensity': 'mean',
                                              'daily_calories_burned': 'mean'})

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
