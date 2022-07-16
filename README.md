# Doel
Een POC om te spelen met containers in ACI, ML, Python en Github Actions.<br>
Train volledig geautomatiseerd een (logistisch regressie) model en implementeer die in ACI.

## Instructies

### Vooraf regelen:
- Azure Container Registry
- Cloud Shell (eventueel een storage account hiervoor inrichten)

### Voer uit:
- Haal het resource ID van de resource group op
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
| ----------------- |:-----------------:|
| AZURE_CREDENTIALS| 	The entire JSON output from the service principal creation step |
| REGISTRY_LOGIN_SERVER| 	The login server name of your registry (all lowercase). Example: myregistry.azurecr.io |
| REGISTRY_USERNAME| 	The clientId from the JSON output from the service principal creation |
| REGISTRY_PASSWORD| 	The clientSecret from the JSON output from the service principal creation |
| RESOURCE_GROUP| 	The name of the resource group you used to scope the service principal |


### En dan nu:
Build de docker container vanuit VSCode (rechter muisklik op de Dockerfile en selecteer *Build Image*)<br>
Gebruik de Docker extensie in VSCode om het image testen in Docker Desktop.
- Start de container
- Open een browser

Je kunt nu een test API call uitvoeren om te bepalen of FastAPI werkt: `http://127.0.0.1:8000/`<br>
Dit levert als het goed is gegaan de volgende output: ```{"message":"FastAPI zegt Hallo Wereld"}```<br>
Je kan ook direct gebruik maken van de Swagger UI: `http://127.0.0.1:8000/docs`<br>
Vanuit de getoonde UI kan de API worden getest.

### ACI
### Deployment van de container
De container kan eenvoudig in Azure worden uitgerold.<br>
Kies na inloggen op de homepage van de Azure Portal voor *Container Instances* en werk door de formulieren heen.<br><br>
![image](https://user-images.githubusercontent.com/57792298/178724259-95822596-65dd-4107-9498-d07c2c46da26.png)<br><br><br>
![image](https://user-images.githubusercontent.com/57792298/178724437-893c810b-0a1c-4d15-8508-8b815f6681f6.png)<br><br><br>
![image](https://user-images.githubusercontent.com/57792298/178724937-980237a4-4fc9-43c3-8af1-7ff265ff99d0.png)<br><br><br>
![image](https://user-images.githubusercontent.com/57792298/178725083-46d3cfb7-5e8a-4789-8e3b-24143d993a33.png)<br><br>
Belangrijk! Voeg bij Networking poort *8000/tcp* toe, hierop luistert de app in de container. Port mappings zoals in Docker zijn in Azure Container Instances (nog) niet mogelijk. Vergeet ook niet een *DNS name label* op te geven zodat je de container kan aanroepen. Hierna kan je op *Review + create* klikken en na de validatie op *Create*. Het kan soms even duren voordat de container is gedeployed. Er zal een resource group worden gemaakt met daarin de container instance.<br><br>
![image](https://user-images.githubusercontent.com/57792298/178725661-f0133755-de4f-4228-a383-7a5d8f21bc28.png)<br><br>
Klik op *Go to resource*. Op het volgende scherm in de rechter kolom vind je de FQDN om de container te kunnen benaderen. In dit voorbeeld:<br><br>
![image](https://user-images.githubusercontent.com/57792298/178725927-991438a9-f87b-45cc-86da-dd881635638f.png)<br><br>
Je kan de container dus aanroepen met: `http://containerpoc.westeurope.azurecontainer.io:8000/`<br>
De aanroep naar de root context zal weer de simpele boodschap tonen; ```{"message":"FastAPI zegt Hallo Wereld"}```. Om het model te testen is de eenvoudigste methode om de de API call via de Swagger UI (```/docs```) uit te voeren. Met curl kom je er ook. De swagger UI geeft hiervoor een voorbeeld na het aanroepen van de API.<br><br>
![image](https://user-images.githubusercontent.com/57792298/178722957-3232853e-1889-4d1a-8180-adfa48c324be.png)<br><br>

### Gebruik van de container
Om de API call te kunnen testen klik je op ```POST /predict Predict Bankbiljet``` balk.<br><br>
![image](https://user-images.githubusercontent.com/57792298/178727346-20b3326b-e23f-4e2a-a47e-2f9b221102b1.png)<br><br>
Klik op *Try it out* en vul wat getallen in (dat mogen integers en floats zijn).<br><br>
![image](https://user-images.githubusercontent.com/57792298/178727631-9d2197d4-38f6-4f8c-9e35-dab46781b736.png)<br><br>
Klik daarna op *Execute* en scrol een stukje naar beneden totdat je de server response ziet.<br><br>
![image](https://user-images.githubusercontent.com/57792298/178727910-00db5d50-ebb8-4ad5-b48f-1b70ae07332f.png)<br><br>
Voor de ingevulde waarden heeft het model voorspeld dat het een goed bankbiljet is.

Voor meer informatie over het gebruik van [FastAPI](https://fastapi.tiangolo.com/ "FastAPI documentatie") is goede documentatie beschikbaar.

### De Data set
De dataset komt van de UCI Machine Learning Repository:

https://archive.ics.uci.edu/ml/datasets/banknote+authentication

Data Set Information:<br>
Data were extracted from images that were taken from genuine and forged banknote-like specimens. For digitization, an industrial camera usually used for print inspection was used. The final images have 400x 400 pixels. Due to the object lens and distance to the investigated object gray-scale pictures with a resolution of about 660 dpi were gained. Wavelet Transform tool were used to extract features from images.
