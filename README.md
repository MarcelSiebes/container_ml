# Instructies
### Vooraf installeren:
- Docker Desktop
- Anaconda
- VSCode

### Voer uit:
```
conda create -name logistische_regressie
conda activate logistische_regressie
pip install -r conda_requirements.txt
cd workdir
python logistische-regressie.py
mv logistische-regressie.pkl ../app
```

### En dan nu:
Build de docker container vanuit VSCode (rechter muisklik op de Dockerfile en selecteer 'Build Image')<br>
Gebruik de Docker extensie in VSCode om het image testen in Docker Desktop.
- Start de container
- Open een browser

Je kunt nu een test API call uitvoeren om te bepalen of FastAPI werkt: `http://127.0.0.1:8000/`<br>
Dit levert als het goed is gegaan de volgende output: ```{"message":"FastAPI zegt Hallo Wereld"}```<br>
Je kan ook direct gebruik maken van de Swagger UI: `http://127.0.0.1:8000/docs`<br>
Vanuit de getoonde UI kan de API eenvoudig worden getest.

### ACI
De container kan eenvoudig in Azure worden uitgerold. Kies na inloggen op de homepage van de Azure Portal voor 'Container Instances' en werkt door de formulieren heen. Er zal een resource group worden gemaakt met daarin de container instance.<br>
Belangrijk! Voeg bij Networking poort *8000/tcp* toe, hierop luistert de app in de container. Port mappings zoals in Docker zijn in Azure (nog) niet mogelijk. Vergeet ook niet een *DNS name label* op te geven zodat je de container kan aanroepen.

![image](https://user-images.githubusercontent.com/57792298/178720962-3a598ee0-1fec-4fc0-b09d-ef245b7b1c41.png)

Na deployment volgens het voorbeeld in het plaatje kan je de container aanroepen met: `http://eennaam.eastus2.azurecontainer.io`

### Data set
De dataset komt van de UCI Machine Learning Repository:

https://archive.ics.uci.edu/ml/datasets/banknote+authentication

Data Set Information:<br>
Data were extracted from images that were taken from genuine and forged banknote-like specimens. For digitization, an industrial camera usually used for print inspection was used. The final images have 400x 400 pixels. Due to the object lens and distance to the investigated object gray-scale pictures with a resolution of about 660 dpi were gained. Wavelet Transform tool were used to extract features from images.
