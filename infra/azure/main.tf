resource "azurerm_resource_group" "rg" {
  name     = "${var.project_name}-rg"
  location = var.location
}
output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}
data "azurerm_client_config" "current" {}
# Storage Account
resource "azurerm_storage_account" "storage" {
  name                     = "${var.project_name}sa"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  allow_nested_items_to_be_public = false
}

# Blob Container for driver photos
resource "azurerm_storage_container" "photos" {
  name                  = "driver-photos"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"
}

# Blob Container for trip logs
resource "azurerm_storage_container" "trips" {
  name                  = "trip-logs"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"
}

output "storage_account_name" {
  value = azurerm_storage_account.storage.name
}
# Key Vault
resource "azurerm_key_vault" "kv" {
  name                = "saferoutepluskvci"
  location            = var.location
  resource_group_name = azurerm_resource_group.rg.name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id

    secret_permissions = [
      "Get", "List", "Set", "Delete", "Purge", "Recover"
    ]
  }
}

output "key_vault_name" {
  value = azurerm_key_vault.kv.name
}
