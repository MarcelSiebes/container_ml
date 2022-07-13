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
Build de docker container vanuit VSCode (rechter muisklik op de Dockerfile en selecteer 'Build Image')

Gebruik de Docker extensie in VSCode om het image testen in Docker Desktop.
- Start de container
- Open een browser

Je kunt nu een test API call uitvoeren om te bepalen of FastAPI werkt: `http://127.0.0.1:8000/`

Dit levert als het goed is gegaan de volgende output: ```{"message":"FastAPI zegt Hallo Wereld"}```
	
Je kan ook direct gebruik maken van de Swagger UI: `http://127.0.0.1:8000/docs`

Vanuit de getoonde UI kan de API eenvoudig worden getest.
