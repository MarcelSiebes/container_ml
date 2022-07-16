"""
@author: 'Marcel Siebes'
"""

#
# API definitie met FastAPI
#

# Library imports
import numpy as np
import pandas as pd
import uvicorn
from fastapi import FastAPI
import pickle

# Class definitie met daarin de call parameters, handig voor pydantic
from bankbiljetten import bankbiljet

# Definieer een FastAPI applicatie
app = FastAPI()

# Laadt het model in
logistische_regressie_pickle = open("logistische-regressie.pkl", "rb")
logistische_regressie = pickle.load(logistische_regressie_pickle)

#
# De verschillende API call definities
#

# Een test API call
@app.get('/')
def index():
    return {'message': 'FastAPI zegt Hallo Wereld'}

# API call voor het gebruik van het model
@app.post('/predict')
def predict_bankbiljet(data:bankbiljet):
    # Lees de binnenkomende data in
    data = data.dict()
    variance = data['variance']
    skewness = data['skewness']
    curtosis = data['curtosis']
    entropy = data['entropy']

    # Doe de logistische regressie
    prediction = logistische_regressie.predict([[variance, skewness, curtosis, entropy]])

    # Indien de uitkomst hoger dan 0.5 is dan verklaren we het biljet vals
    if(prediction[0] > 0.5 ): prediction_resultaat = "Vals bankbiljet"
    else: prediction_resultaat = "Goed bankbiljet"
    return {
        'prediction': prediction_resultaat
    }

# Main
if __name__ == '__main__':
    uvicorn.run(app, host = '0.0.0.0', port = 8000)
