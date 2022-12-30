import numpy as np


def replace_id(df):
    """
    Replaces the id in the dataframe with smaller integer numbers
    :param df:
    :return:
    """
    # Replace the id of dataframe to a range from 1:33
    id_index = dict(zip(df['id'].unique(), np.arange(1, 34)))

    # For every row in id
    for ids in df['id'].unique():

        # Replace the id with small index numbers from 1-33
        df['id'] = df['id'].replace(ids, id_index[ids])

    return df
