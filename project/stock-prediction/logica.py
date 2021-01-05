from keras.models import model_from_json
from pandas_datareader._utils import RemoteDataError
from sklearn import preprocessing
import numpy as np
from sklearn.externals import joblib


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


def data_prediction(panel_data):
    data = panel_data.copy()
    model_file = 'model/deeplearningmodel.json'
    json_file = open(model_file, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    weight_file = 'model/model.h5'
    loaded_model.load_weights(weight_file)
    print("Loaded model from disk")

    history_points = 60
    data['Close'] = data['Adj Close']
    data = data[['High', 'Low', 'Close', 'Volume', 'Open']]
    scaler = preprocessing.MinMaxScaler()
    data_normalised = preprocessing.MinMaxScaler().fit_transform(data)
    trunced_data_normalised = np.array(data_normalised[-history_points:])

    next_day_open_values = np.array(data.iloc[:, -1][history_points:])
    next_day_open_values = np.expand_dims(next_day_open_values, -1)
    scaler.fit(next_day_open_values)
    result = loaded_model.predict(np.array([trunced_data_normalised]))

    return scaler.inverse_transform(result)[0][0]


