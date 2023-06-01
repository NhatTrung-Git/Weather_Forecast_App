import pickle
import os
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV, train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.base import BaseEstimator
from sklearn.metrics import mean_squared_error
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, LSTM
from tensorflow.python.keras.optimizers import adam_v2

def RunDecisionTre(df, location):
    x = df[['Temp', 'Wind', 'Direction', 'Humidity', 'Barometer']]
    y = df['Weather']

    x_train, _, y_train, _ = train_test_split(x, y, test_size=0.3, random_state=42)

    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)

    param_dist = {
        'max_depth': [None] + list(np.random.randint(1, 20, size=10)),
        'min_samples_split': np.random.randint(2, 20, size=10),
        'min_samples_leaf': np.random.randint(1, 10, size=10),
    }
    
    model = DecisionTreeClassifier(criterion='entropy')
    random_search = RandomizedSearchCV(estimator=model, param_distributions=param_dist, cv=5)
    random_search.fit(x_train_scaled, y_train)

    best_params = random_search.best_params_
    best_model = DecisionTreeClassifier(criterion='entropy', **best_params)

    best_model.fit(x_train_scaled, y_train)
    
    absolutePath = os.path.join(os.getcwd(), location + '.pkl')
    pickle.dump(best_model, open(absolutePath, 'wb'))
    
def RunSVM(df, location):
    x = df[['Temp', 'Wind', 'Direction', 'Humidity', 'Barometer']]
    y = df['Weather']

    x_train, _, y_train, _ = train_test_split(x, y, test_size=0.3, random_state=42)

    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)

    model = SVC(random_state=42)

    param_grid = {
        'C': [0.1,1, 10, 100], 
        'gamma': [1,0.1,0.01,0.001],
        'kernel': ['rbf', 'poly', 'sigmoid']
    }

    grid_search = GridSearchCV(model, param_grid, cv=3)
    grid_search.fit(x_train_scaled, y_train)

    best_params = grid_search.best_params_

    best_model = SVC(C=best_params['C'], kernel=best_params['kernel'], gamma=best_params['gamma'], random_state=42)
    best_model.fit(x_train_scaled, y_train)
    
    absolutePath = os.path.join(os.getcwd(), location + '.pkl')
    pickle.dump(best_model, open(absolutePath, 'wb'))

def RunMLP(df, location):
    x = df[['Temp', 'Wind', 'Direction', 'Humidity', 'Barometer']]
    y = df['Weather']

    x_train, _, y_train, _ = train_test_split(x, y, test_size=0.3, random_state=42)
    
    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    
    model = MLPClassifier(random_state=42)

    param_grid = {
        'hidden_layer_sizes': [(2,), (10,), (50,50), (25,25,25)],
        'activation': ['logistic', 'relu'],
        'alpha': [0.0001, 0.001, 0.01, 0.05],
        'solver': ['sgd', 'adam'],
        'learning_rate': ['constant','adaptive'],
    }

    grid_search = GridSearchCV(model, param_grid, cv=5)
    grid_search.fit(x_train_scaled, y_train)

    best_params = grid_search.best_params_
    
    best_model = MLPClassifier(hidden_layer_sizes=best_params['hidden_layer_sizes'], activation=best_params['activation'], alpha=best_params['alpha'], random_state=42)
    best_model.fit(x_train_scaled, y_train)
    
    absolutePath = os.path.join(os.getcwd(), location + '.pkl')
    pickle.dump(best_model, open(absolutePath, 'wb'))
    
class KerasRegressor(BaseEstimator):
    def __init__(self, units=50, epochs=50, batch_size=32, time_steps=1):
        self.units = units
        self.epochs = epochs
        self.batch_size = batch_size
        self.time_steps = time_steps
        self.model = None
    
    def fit(self, X, y):
        model = Sequential()
        model.add(LSTM(units=self.units, input_shape=(self.time_steps, 1)))
        model.add(Dense(units=1))
        model.compile(optimizer=adam_v2.Adam(), loss='mean_squared_error')
        self.model = model
        self.model.fit(X, y, epochs=self.epochs, batch_size=self.batch_size)
        return self
    
    def predict(self, X):
        return self.model.predict(X)

def CreateDataset(dataset, time_steps=1):
    x, y = [], []
    
    for i in range(len(dataset) - time_steps):
        a = dataset[i:(i + time_steps), 0]
        x.append(a)
        y.append(dataset[i + time_steps, 0])
        
    return np.array(x), np.array(y)

def RunLSTM(df, location, fileName, timeSteps):
    df = df[['Temp', 'Wind', 'Direction', 'Humidity', 'Barometer']]
    
    for c in df.columns:    
        dataset = df[c].values
        scaler = MinMaxScaler(feature_range=(0, 1))
        dataset = scaler.fit_transform(dataset.reshape(-1, 1))
        x, y = CreateDataset(dataset, timeSteps)
        train_size = int(len(x) * 0.7)
        x_train = x[:train_size]
        y_train = y[:train_size]
        param_grid = {'units': [50, 100, 150], 'epochs': [50, 100, 150], 'batch_size': [32, 64, 128]}
        grid_search = GridSearchCV(estimator=KerasRegressor(time_steps=timeSteps), param_grid=param_grid, cv=3, scoring='neg_mean_squared_error')
        grid_search.fit(x_train, y_train)
        best_model = grid_search.best_estimator_
        
        absolutePath = os.path.join(os.getcwd(), location + c + '_' + fileName + '.pkl')
        pickle.dump(best_model, open(absolutePath, 'wb'))

def LoadModel(filePath):
    return pickle.load(open(filePath, 'rb'))
