"""
@author: 'Marcel Siebes'
"""

# Library imports
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegressionCV
import pickle

# Lees de data en sla die op in een pandas dataframe
df = pd.read_csv("data/BankNote_Authentication.csv")

# Selecteer de predictors en target
x = df.iloc[:,:-1]
y = df.iloc[:,-1]

# Maak een scaler object
std_scaler = StandardScaler()

# Normaliseer de data
x_std = pd.DataFrame(std_scaler.fit_transform(x), columns=x.columns)
x_std

# Controleer op missende waardes in x
print(x_std.isnull().sum())

# Controleer op missende waardes in y
print(y.isnull().sum())

# Split de data in een training en test set
x_train, x_test, y_train, y_test = train_test_split(x_std,y, test_size = 0.3, random_state = 0)

# Implementeer Logistische Regressie met ingebouwde cross-validation
logistische_regressie = LogisticRegressionCV(cv=10)
logistische_regressie.fit(x_train, y_train)

# Predict de target van de test set
y_pred = logistische_regressie.predict(x_test)

# Bepaal de AUC score
score = roc_auc_score(y_test, y_pred)
score

# Voorbeeld van een vals bankbiljet
logistische_regressie.predict([[-2, -3, 1.1, 2.41]])

# Voorbeeld van een goed bankbiljet
logistische_regressie.predict([[2, 3, 4, 1]])

# Maak een Pickle file (serialization) voor gebruik in de container
pickle_file = open("logistische-regressie.pkl", "wb")
pickle.dump(logistische_regressie, pickle_file)
pickle_file.close()