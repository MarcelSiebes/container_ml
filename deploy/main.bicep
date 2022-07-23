@description('Neem de lokatie van de resource group over')
param location string = resourceGroup().location

@description('ACR naam prefix')
param containerRegistryPrefix string

@description('Toegestaande SKU soorten')
@allowed([
  'Basic'
])
param sku string

var containerRegistryName = '${containerRegistryPrefix}${uniqueString(resourceGroup().id)}'

resource acr 'Microsoft.ContainerRegistry/registries@2021-09-01' = {
  name: containerRegistryName
  location: location
  sku: {
    name: sku
  }
}

@description('Output the login server property for later use')
output loginServer string = acr.properties.loginServer
