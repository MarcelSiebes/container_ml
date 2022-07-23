@description('Neem de lokatie van de resource group over')
param location string = resourceGroup().location

var containerRegistryName = '${uniqueString(resourceGroup().id)}'

resource acr 'Microsoft.ContainerRegistry/registries@2021-09-01' = {
  name: containerRegistryName
  location: location
  sku: {
    name: 'Basic'
  }
}

@description('Output the login server property for later use')
output loginServer string = acr.properties.loginServer
