data "azurerm_resource_group" "rg" {
  name = "rg-niharika-rajput"
}

#datalake
resource "azurerm_storage_account" "data" {
  name                        = var.datalake_name
  location                    = var.location
  resource_group_name         = "rg-niharika-rajput"
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
  resource_group_name          = "rg-niharika-rajput"
  location                     = var.location
  version                      = "12.0"
  administrator_login          = "Niha"
  administrator_login_password = "Kangra@123"   #manually create a key vault
  tags = {
    environment = "development"
  }
}

#database
resource "azurerm_sql_database" "gp" {
  name                = var.database_name
  resource_group_name = "rg-niharika-rajput"
  location            = var.location
  server_name         = var.server_name
  collation           = "SQL_Latin1_General_CP1_CI_AS"
  zone_redundant      = false
  
  tags = {
    Environment = "development"
  }
}
