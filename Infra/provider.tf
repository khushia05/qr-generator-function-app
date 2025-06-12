terraform {
  backend "azurerm" {
    storage_account_name = "sakhushitfstate01"
    container_name       = "tfstate"
  }
}
