import datetime
import math

import numpy as np
from pandas_datareader._utils import RemoteDataError
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression, Ridge, Lasso, BayesianRidge, LassoLars, \
    OrthogonalMatchingPursuit, ARDRegression, SGDRegressor
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures


def data_retrieve(df):
    try:
        close_px = df['Adj Close']

        # Calculate rets
        rets = close_px / close_px.shift(1) - 1

        # Provide data to Flask app
        return close_px.index.format(formatter=lambda x: x.strftime('%Y-%m-%d')), \
               close_px.to_list(), \
               rets.to_list()

    # If any error, provide back to flask app, although it does not work properly.
    except TypeError as e:
        return e
    except NameError as e:
        return e
    except Exception as e:
        return e
    except RemoteDataError as e:
        return e


def data_prediction(data):
    df = data
    pass
