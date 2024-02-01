data "azurerm_resource_group" "rg" {
  name = "rg-xxx"
}

#datalake
resource "azurerm_storage_account" "data" {
  name                        = var.datalake_name
  location                    = var.location
  resource_group_name         = "rg-xxx"
  account_kind                = "StorageV2"
  account_tier                = "Standard"
  account_replication_type    = "LRS"

 tags = {
    environment = "development"
  }
}

#database-server
resource "azurerm_sql_server" "example" {
  name                         = var.server_name
  resource_group_name          = "rg-xxx"
  location                     = var.location
  version                      = "12.0"
  administrator_login          = "xx"
  administrator_login_password = "xxxx"   #manually create a key vault
  tags = {
    environment = "development"
  }
}

#database
resource "azurerm_sql_database" "gp" {
  name                = var.database_name
  resource_group_name = "rg-xx"
  location            = var.location
  server_name         = var.server_name
  collation           = "SQL_Latin1_General_CP1_CI_AS"
  zone_redundant      = false
  
  tags = {
    Environment = "development"
  }
}
