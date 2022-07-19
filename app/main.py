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

# Class definitie met daarin de call parameters, pydantic is handig
# https://pydantic-docs.helpmanual.io/
from bankbiljetten import bankbiljet

# Definieer een FastAPI applicatie
app = FastAPI()

# Laadt het model in
model_pickle = open("/app/model.pkl", "rb")
model = pickle.load(model_pickle)

#
# Een laat API call definities
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
    prediction = model.predict_proba([[variance, skewness, curtosis, entropy]])

    # Indien de uitkomst hoger dan 0.5 is dan verklaren we het bankbiljet vals
    if(prediction[0] > 0.5): prediction_result = "Vals bankbiljet"
    else: prediction_result = "Goed bankbiljet"
    return {
        'prediction': prediction_result, 'confidence': prediction[0]
    }

# Main
if __name__ == '__main__':
    uvicorn.run(app, host = '0.0.0.0', port = 8000)
