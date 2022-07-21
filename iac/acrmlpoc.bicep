targetScope =  'resourceGroup'

resource acrmlpoc 'Microsoft.ContainerRegistry/registries@2021-09-01' = {
  name: 'acrpoc'
  location: resourceGroup().location
}
