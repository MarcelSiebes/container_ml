"""
@author: 'Marcel Siebes'
"""

# imports
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix, classification_report
from sklearn.svm import SVC
import pickle

# Lees de data en sla die op in een pandas dataframe
df = pd.read_csv("workdir_model_training/data/BankNote_Authentication.csv")

# Eerst wat elementaire data inzichten tonen
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

# Split de data in een training en test set: 70% training en 30% test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 0)

# Implementeer een support vector machine met een poly kernel zoals in het artikel
model = SVC(kernel='poly', degree=3, probability=True)
model.fit(X_train, y_train)

# Predict de target van de test set
y_pred = model.predict(X_test)

# Bepaal de AUC score, classificatie rapport en de confusion matrix
score = accuracy_score(y_test, y_pred)
print("AUC Score {}", score)
print(classification_report(y_test, y_pred))
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Maak een Pickle file van het getrainde model voor gebruik in de container
pickle_file = open("model.pkl", "wb")
pickle.dump(model, pickle_file)
print(f"Model opgeslagen met de parameters: {pickle_file.params}")
pickle_file.close()
