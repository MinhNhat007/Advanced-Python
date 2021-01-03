import pandas_datareader.data as web
from pandas_datareader._utils import RemoteDataError
import requests


def data(symbol, source, start, end):
    try:
        df = web.DataReader(symbol, source, start, end)

        return df
    except TypeError as e:
        return e
    except NameError as e:
        return e
    except Exception as e:
        return e
    except RemoteDataError as e:
        return e


def get_symbol(symbol):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)

    result = requests.get(url).json()

    return result['ResultSet']['Result'][0]['name']
