# Import the plotly library
import plotly.express as px
from plotly.subplots import make_subplots


# Create function for plotting the correlation of variables
def plot_corr(corr_values):
    """
    Takes in an array of values and returns a correlation heat map plot
    """

    fig = px.imshow(corr_values, text_auto=True)
    fig.show()


def bar_chart(df, x=None, y=None, x_label=None, y_label=None, col=None):
    """
    Takes in a dataframe and plot a bar chart based on filter condition of x and y
    """

    if col is None:
        col = df.columns[1]

    fig = px.bar(data_frame=df, x=x, y=y, color=col).update_layout(
        xaxis=dict(title=x_label), yaxis=dict(title=y_label)
    )
    fig.show()



