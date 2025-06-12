Connect-AzAccount

$resourceGroupName  = "rg-khushi-tfstate-01"
$location           = "West Europe"
$storageAccountName = "sakhushitfstate01"
$subscriptionId     = "bac17140-4441-497d-98ab-773124840802"

# Create RG and storage account in order to store state file for terraform during pipeline run.

New-AzResourceGroup -Name $resourceGroupName -Location $location

New-AzStorageAccount -ResourceGroupName $resourceGroupName  -Name $storageAccountName  -SkuName Standard_LRS  -Location $location -Kind StorageV2

$context = New-AzStorageContext -StorageAccountName $storageAccountName -UseConnectedAccount
New-AzStorageContainer -Name "tfstate" -Context $context -Permission Off

# Create a service principle in order to run terraform through Github action not against user account

$sp = New-AzADServicePrincipal -DisplayName "sp-appreg-khushi-01"

New-AzRoleAssignment -ObjectId $sp.Id -RoleDefinitionName "Contributor" -Scope "/subscriptions/$subscriptionId"

# Fetch Client ID and Cleint Secret using below command during script exevcution

# $sp.AppId  # Client ID
# $sp.PasswordCredentials.SecretText  # Client Secret (store securely)
# $sp.TenantId  # Tenant ID