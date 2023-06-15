import joblib
import os
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV, train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import mean_squared_error
from tensorflow.python.keras.models import Sequential, load_model
from tensorflow.python.keras.layers import Dense, LSTM

def RunDecisionTree(df, location, fileName):
    x = df[['Temp', 'Wind', 'Direction', 'Humidity', 'Barometer']]
    y = df['Weather']

    x_train, _, y_train, _ = train_test_split(x, y, test_size=0.3, random_state=42)

    # scaler = StandardScaler()
    # x_train_scaled = scaler.fit_transform(x_train)

    param_dist = {
        'max_depth': [None] + list(np.random.randint(1, 20, size=10)),
        'min_samples_split': np.random.randint(2, 20, size=10),
        'min_samples_leaf': np.random.randint(1, 10, size=10),
    }
    
    model = DecisionTreeClassifier(criterion='entropy')
    random_search = RandomizedSearchCV(estimator=model, param_distributions=param_dist, cv=5)
    # random_search.fit(x_train_scaled, y_train)
    random_search.fit(x_train, y_train)

    best_params = random_search.best_params_
    best_model = DecisionTreeClassifier(criterion='entropy', **best_params)

    # best_model.fit(x_train_scaled, y_train)
    best_model.fit(x_train, y_train)
    
    absolutePath = os.getcwd() + location + fileName + '.pkl'
    joblib.dump(best_model, open(absolutePath, 'wb'))
    
def RunSVM(df, location, fileName):
    x = df[['Temp', 'Wind', 'Direction', 'Humidity', 'Barometer']]
    y = df['Weather']

    x_train, _, y_train, _ = train_test_split(x, y, test_size=0.3, random_state=42)

    # scaler = StandardScaler()
    # x_train_scaled = scaler.fit_transform(x_train)

    model = SVC(random_state=42)

    param_grid = {
        'C': [0.1,1, 10, 100], 
        'gamma': [1,0.1,0.01,0.001],
        'kernel': ['rbf', 'poly', 'sigmoid']
    }

    grid_search = GridSearchCV(model, param_grid, cv=3)
    # grid_search.fit(x_train_scaled, y_train)
    grid_search.fit(x_train, y_train)

    best_params = grid_search.best_params_

    best_model = SVC(C=best_params['C'], kernel=best_params['kernel'], gamma=best_params['gamma'], random_state=42)
    # best_model.fit(x_train_scaled, y_train)
    best_model.fit(x_train, y_train)
    
    absolutePath = os.getcwd() + location + fileName + '.pkl'
    joblib.dump(best_model, open(absolutePath, 'wb'))

def RunMLP(df, location, fileName):
    x = df[['Temp', 'Wind', 'Direction', 'Humidity', 'Barometer']]
    y = df['Weather']

    x_train, _, y_train, _ = train_test_split(x, y, test_size=0.3, random_state=42)
    
    # scaler = StandardScaler()
    # x_train_scaled = scaler.fit_transform(x_train)
    
    model = MLPClassifier(random_state=42)

    param_grid = {
        'hidden_layer_sizes': [(2,), (10,), (50,50), (25,25,25)],
        'activation': ['logistic', 'relu'],
        'alpha': [0.0001, 0.001, 0.01, 0.05],
        'solver': ['sgd', 'adam'],
        'learning_rate': ['constant','adaptive'],
    }

    grid_search = GridSearchCV(model, param_grid, cv=5)
    # grid_search.fit(x_train_scaled, y_train)
    grid_search.fit(x_train, y_train)

    best_params = grid_search.best_params_
    
    best_model = MLPClassifier(hidden_layer_sizes=best_params['hidden_layer_sizes'], activation=best_params['activation'], alpha=best_params['alpha'], random_state=42)
    # best_model.fit(x_train_scaled, y_train)
    best_model.fit(x_train, y_train)
    
    absolutePath = os.getcwd() + location + fileName + '.pkl'
    joblib.dump(best_model, open(absolutePath, 'wb'))
    
def BuildModel(units, time_steps):
    model = Sequential()
    model.add(LSTM(units=units, activation='relu', input_shape=(time_steps, 5)))
    model.add(Dense(units=5))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def CreateDataset(dataset, time_steps=1):
    x, y = [], []

    for i in range(len(dataset) - time_steps):
        a = dataset[i:(i + time_steps), :]
        x.append(a)
        y.append(dataset[i + time_steps, :])

    return np.array(x), np.array(y)

def CreateDatasetWithDates(dataset, dataDates, time_steps=1):
    x, y, dates = [], [], []

    for i in range(len(dataset) - time_steps):
        a = dataset[i:(i + time_steps), :]
        x.append(a)
        y.append(dataset[i + time_steps, :])
        dates.append(dataDates[i + time_steps, 0])

    return np.array(x), np.array(y), np.array(dates)

def CreateX(dataset, time_steps=1):
    x = []
    
    for i in range(len(dataset) - time_steps):
        a = dataset[i:i + time_steps, :]
        x.append(a)

    return np.array(x)

def RunLSTM(df, location, fileName, time_steps):
    df = df[['Temp', 'Wind', 'Direction', 'Humidity', 'Barometer']]
    param_grid = {'units': [50, 100, 150], 'batch_size': [32, 64, 128], 'epochs': [50, 100, 150]}

    dataset = df.values
    # scaler = MinMaxScaler(feature_range=(0, 1))
    # dataset = scaler.fit_transform(dataset)
    x, y = CreateDataset(dataset, time_steps)
    train_size = int(len(x) * 0.7)
    x_train = x[:train_size]
    y_train = y[:train_size]
    x_train = x_train.reshape((x_train.shape[0], x_train.shape[1], x_train.shape[2]))

    best_model = None
    best_mse = float('inf')

    for units in param_grid['units']:
        model = BuildModel(units, time_steps)

        for batch_size in param_grid['batch_size']:
            for epochs in param_grid['epochs']:
                model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, verbose=0)
                y_pred = model.predict(x_train)
                mse = mean_squared_error(y_train, y_pred)

                if mse < best_mse:
                    best_mse = mse
                    best_model = model

    absolutePath = os.getcwd() + location + fileName + '.h5'
    best_model.save(absolutePath)


def LoadModel(filePath):
    return joblib.load(open(filePath, 'rb'))

def LoadLSTM(filePath):
    return load_model(filePath)

def CalScore(df, model):
    x = df[['Temp', 'Wind', 'Direction', 'Humidity', 'Barometer']]
    y = df['Weather']

    _, x_test, _, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
    
    return model.score(x_test, y_test)

def GetPredictedAndActualValues(df, modelPath):
    x = df[['Temp', 'Wind', 'Direction', 'Humidity', 'Barometer']]
    y = df['Weather']
    
    size = 100 / len(df)
    
    if size > 1:
        size = 0.9

    # x_train, x_test, _, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
    _, x_test, _, y_test = train_test_split(x, y, test_size=size, random_state=42)
    # scaler = StandardScaler()
    # scaler.fit_transform(x_train)
    # x_test_scaled = scaler.transform(x_test)
    
    model = LoadModel(modelPath)
    # y_pred = model.predict(x_test_scaled)
    y_pred = model.predict(x_test)
    
    return y_test, y_pred, str(type(model)).split("'")[1].split(".")[len(str(type(model)).split("'")[1].split(".")) - 1]

def GetPredictedAndActualValuesLSTM(df, modelPath):
    dataset = df[['Temp', 'Wind', 'Direction', 'Humidity', 'Barometer']].values
    dataDate = df[['Date']].values
    # scaler = MinMaxScaler(feature_range=(0, 1))
    # dataset = scaler.fit_transform(dataset)

    model = LoadLSTM(modelPath)
    x, y, dates = CreateDatasetWithDates(dataset, dataDate, model.input_shape[1])
    
    size = 1 - 100 / len(df)
    
    if size > 1:
        size = 0.9

    # train_size = int(len(x) * 0.8)
    train_size = int(len(x) * size)
    x_test = x[train_size:]
    y_test = y[train_size:]
    dates_test = dates[train_size:]
    x_test = x_test.reshape((x_test.shape[0], x_test.shape[1], x_test.shape[2]))

    y_pred_test = model.predict(x_test)
    # y_pred_test = scaler.inverse_transform(y_pred_test)

    return y_test, y_pred_test, dates_test

def GetPredictedValue(df, model, lstm, time_steps):
    lastDate = df['Date'].tail(1).values[0]
    data = df.tail(lstm.input_shape[1] * (time_steps + 1)).reset_index(drop=True)
    data = data[['Temp', 'Wind', 'Direction', 'Humidity', 'Barometer']]
    x = CreateX(data.values, lstm.input_shape[1])
    x = x.reshape((x.shape[0], x.shape[1], x.shape[2]))
    predictValues = lstm.predict(x)
    predictedDF = pd.DataFrame(predictValues.reshape(-1, 5), columns=['Temp', 'Wind', 'Direction', 'Humidity', 'Barometer'])
    predictedDF['Weather'] = model.predict(predictedDF)
    predictedDF['Date'] = lastDate + pd.to_timedelta((predictedDF.index + 1) * 30, unit='minutes')
    return predictedDF[['Date', 'Weather', 'Temp', 'Wind', 'Direction', 'Humidity', 'Barometer']]