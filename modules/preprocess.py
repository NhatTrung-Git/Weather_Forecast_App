import pandas as pd
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import train_test_split


def Preprocessing(DATA):
    if DATA['Date'].dtypes == object:
        DATA = DATA.astype({'Date':'string'})
        DATA['Date'] = pd.to_datetime(DATA['Date'].str.strip(), format='%Y%m%d %H:%M')
        
    if DATA['Weather'].dtypes == object:
        DATA = DATA.astype({'Weather':'string'})
    
    if DATA['Direction'].dtypes == object:
        DATA['Direction'] = DATA['Direction'].str.extract(r'(-?\d+)').astype(float)
        
    if 'Visibility' in DATA.columns:
        DATA.drop(['Visibility'], axis=1, inplace=True)
        
    DATA['Wind'] = DATA['Wind'].fillna(0)
    DATA.sort_values(by=['Date'], inplace=True)
    DATA.dropna(inplace=True)
    DATA.drop_duplicates(inplace=True)
    subsetData = DATA[['Temp', 'Wind', 'Direction', 'Humidity', 'Barometer']]
        
    for column in subsetData.columns:
        Q1 = DATA[column].quantile(0.25)
        Q3 = DATA[column].quantile(0.75)
        IQR = Q3 - Q1
        lowerThreshold = Q1 - 1.5 * IQR
        upperThreshold = Q3 + 1.5 * IQR
        DATA = DATA[(DATA[column] >= lowerThreshold) & (DATA[column] <= upperThreshold)]
        
    DATA = DATA.reset_index(drop=True)
    return DATA

def CalFeatureScores(DATA):
    x = DATA[['Temp', 'Wind', 'Direction', 'Humidity', 'Barometer']]
    y = DATA['Weather']
    x_train, _, y_train, _ = train_test_split(x, y, test_size=0.2, random_state=42)

    selector = SelectKBest(score_func=f_classif, k=5)
    selector.fit(x_train, y_train)
    featureScores = selector.scores_
    scoresDF = pd.DataFrame({'Feature': x.columns, 'Score': featureScores})
    scoresDF = scoresDF.sort_values(by='Score', ascending=False)
    
    return scoresDF