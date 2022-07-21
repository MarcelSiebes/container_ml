targetScope = 'subscription'

resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: 'rgmlpoc'
  location: 'westeurope'
}

module acr 'acrmlpoc.bicep' = {
  name: 'acrpoc'
  scope: rg
}
