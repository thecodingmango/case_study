# Import the stats model library for linear regression
import statsmodels
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
import numpy as np


# Create a function that fits the linear regression model
def lm_model(response_variable, explanatory_variable):
    """
    Takes in data from data frame and fit a linear regression model
    :param explanatory_variable: All the explanatory variables that is trying to explain the result
    :param response_variable: The response data that is the result from the explanatory data
    :return: Linear regression model
    """

    explanatory_variable = sm.add_constant(explanatory_variable)

    # Fit the linear regression model
    lm = sm.OLS(response_variable, explanatory_variable).fit()

    return lm


def lm_regularized(response_variable, explanatory_variable, l1, alpha):
    """
    Linear regression model with regularization
    """

    explanatory_variable = sm.add_constant(explanatory_variable)

    # Create linear regression model
    lm = sm.OLS(response_variable, explanatory_variable)
    lm_norm = lm.fit()

    # Fit the regression model with regularization
    lm_reg = lm.fit_regularized(L1_wt=l1, alpha=alpha, start_params=lm_norm.params)
    lm_reg = sm.regression.linear_model.OLSResults(lm, lm_reg.params, lm.normalized_cov_params)

    return lm_reg


def vif(lm):
    """
    Takes in a linear regression model, and outputs the Variance Inflated Factor
    """

    # Saves the linear regression variables in the model
    lm_var = lm.model.exog

    # For each linear regression variables in the model, calculates their VIF values
    variance_factor = [variance_inflation_factor(lm_var, i) for i in range(lm_var.shape[1])]

    return variance_factor


