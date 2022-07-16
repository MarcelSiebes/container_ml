# Doel
MLOps POC - Train, volledig geautomatiseerd, een ML model en implementeer die in ACI. Hierbij wordt gebruik gemaakt van een docker container in ACI en Github Actions.<br>
De code bevat een eenvoudige logistische regressie. Het model is getraind met een UCI dataset. Deze dataset bevat gegevens die verkregen zijn door met een een wavelet transformatie tool features te extraheren van foto's van bankbiljetten. De set bestaat uit gegevens van valse en niet valse bankbiljetten.
Het model zal aan de hand van waardes die worden meegegeven aan vier parameters proberen te bepalen of een bankbiljet vals is of niet. Deze parameters zijn:
- variance,
- skewness,
- curtosis,
- entropy

## Instructies

### Vooraf regelen:
- Azure Container Registry
- Cloud Shell (eventueel een storage account hiervoor inrichten)

#### Voer uit:
- Haal het resource ID van de resource group op waarin de Azure Container Registry is gedefinieerd
```
az group show --name <RESOURCE GROUP NAAM> --query id --output tsv
```

- Maak een Service Principle
```
az ad sp create-for-rbac --scope <RESOURCE ID> --role Contributor --sdk-auth
```
Bewaar de JSON uitvoer, die is nog nodig.

- Haal het resource ID op van de container registry
```
az acr show --name <CONTAINER REGISTRY NAAM> --query id --output tsv
```

- Koppel de AcrPush role (geeft push en pull toegang op de registry)
```
az role assignment create --assignee <CLIENT ID> --scope <REGISTRY ID> --role AcrPush
```

Voeg de onderstaande secrets toe in Github (Settings -> Secrets -> Actions)

| **Secret**        | **Value**         |
| ----------------- |-------------------|
| AZURE_CREDENTIALS | De complete JSON uit de service principal stap |
| REGISTRY_LOGIN_SERVER | De login server naam van de registry |
| REGISTRY_USERNAME | Het clientId uit de JSON uit de service principal stap |
| REGISTRY_PASSWORD | Het clientSecret uit de JSON uit de service principal stap |
| RESOURCE_GROUP | De naam van de resource group gebruikt in de scope van de service principal |


### Use cases van de workflows:
Er zijn drie workflows gedefinieerd met Github Actions. In de onderstaande tabel zijn de triggers uiteengezet.
| **Workflow**        | **Triggers**         | **Vervolg Actie**   |
| ------------------- | -------------------- | ------------------- |
| Retrain Model Workflow | Nieuwe data of data aanpassing | Container Deployment Workflow |
|              | Aanpassing aan het python script of de requirements file | Container Deployment Workflow |
|              | Verwijdering van het getrainde model | Container Deployment Workflow |
| Container Deployment Workflow | Aanpassing Dockerfile | Geen |
|                               | Aanpassing aan de bestanden in de app directory | Geen |
| CodeQL | Iedere push en pull-request naar de main branch | Geen    |

Alle workflows kunnen ook handmatig worden gestart. De Retrain Model Workflow zal ook bij het handmatig starten altijd worden gevolgd door de Container Deployment Workflow.


### Gebruik van de container
Je kan de container aanroepen met ```http://<AZURE URL>.io:8000/```. Wat de Azure URL precies is kan worden opgezocht in het Overview scherm van de betreffende container instance. De aanroep naar de root context zal een simpele boodschap tonen; {"message":"FastAPI zegt Hallo Wereld"}. Om het model te testen is de eenvoudigste methode om de de API call via de Swagger UI /docs uit te voeren. Met curl kom je er ook. De swagger UI geeft hiervoor een voorbeeld na het aanroepen van de API.

Om de API call te kunnen testen klik je op ```POST /predict Predict Bankbiljet``` balk.<br><br>
![image](https://user-images.githubusercontent.com/57792298/178727346-20b3326b-e23f-4e2a-a47e-2f9b221102b1.png)<br><br>
Klik op *Try it out* en vul wat getallen in (dat mogen integers en floats zijn).<br><br>
![image](https://user-images.githubusercontent.com/57792298/178727631-9d2197d4-38f6-4f8c-9e35-dab46781b736.png)<br><br>
Klik daarna op *Execute* en scrol een stukje naar beneden totdat je de server response ziet.<br><br>
![image](https://user-images.githubusercontent.com/57792298/178727910-00db5d50-ebb8-4ad5-b48f-1b70ae07332f.png)<br><br>
Voor de ingevulde waarden heeft het model voorspeld dat het een goed bankbiljet is.<br><br>

Voor meer informatie over het gebruik van [FastAPI](https://fastapi.tiangolo.com/ "FastAPI documentatie") is goede documentatie beschikbaar.

### De Data set
De dataset komt van de [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/banknote+authentication "UCI Machine Learning Repository"):

Data Set Information:<br>
Data were extracted from images that were taken from genuine and forged banknote-like specimens. For digitization, an industrial camera usually used for print inspection was used. The final images have 400x 400 pixels. Due to the object lens and distance to the investigated object gray-scale pictures with a resolution of about 660 dpi were gained. Wavelet Transform tool were used to extract features from images.

### Voor meer informatie:
[Configure a GitHub Action to create a container instance](https://docs.microsoft.com/en-us/azure/container-instances/container-instances-github-action)<br>
[Azure/aci-deploy Github repository](https://github.com/Azure/aci-deploy)
