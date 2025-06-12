terraform {
  backend "azurerm" {
    resource_group_name   = "my-rg"
    storage_account_name  = "mystoragename"
    container_name        = "terraform-state"
    key                   = "terraform.tfstate"
  }
}
