terraform {
  backend "azurerm" {
    resource_group_name   = "rg-khushi-tfstate-01"
    storage_account_name  = "sakhushitfstate01"
    container_name        = "tfstate"
    key                   = "terraform.tfstate"
  }
}
