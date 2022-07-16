"""
@author: 'Marcel Siebes'
"""

# Library imports
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, confusion_matrix, classification_report
from sklearn.linear_model import LogisticRegressionCV
import pickle

# Lees de data en sla die op in een pandas dataframe
df = pd.read_csv("workdir_model_training/data/BankNote_Authentication.csv")

# Eerst wat elementaire data iinzichten tonen
print(df.shape)
print(df.info())
print(df.describe())

# Bekijk of er sprake is van class imbalance
print(df['class'].value_counts())

# Maak een scaler object
scaler = MinMaxScaler() 

# Normaliseer de data (door de MinMaxScaler hoeft de kolom 'class' er niet uit.)
df_norm = scaler.fit_transform(df)
cols = ['variance', 'skewness', 'kurtosis', 'entropy', 'class']
df_norm = pd.DataFrame(df_norm, columns=cols)
df_norm.describe()

# Selecteer de predictors en target
X = df_norm.iloc[:,:-1]
y = df_norm.iloc[:,-1]

# Split de data in een training en test set:. 70% training en 30% test.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)

# Implementeer Logistische Regressie met ingebouwde cross-validation
logistische_regressie = LogisticRegressionCV(cv=10)
logistische_regressie.fit(X_train, y_train)

# Predict de target van de test set
y_pred = logistische_regressie.predict(X_test)

# Bepaal de AUC score en de confusion matrix
score = roc_auc_score(y_test, y_pred)
print("AUC Score {}", score)
print(classification_report(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Maak een Pickle file (serialization) voor gebruik in de container
pickle_file = open("workdir_model_training/logistische-regressie.pkl", "wb")
pickle.dump(logistische_regressie, pickle_file)
pickle_file.close()
