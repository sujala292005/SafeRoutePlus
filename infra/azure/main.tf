resource "azurerm_resource_group" "rg" {
  name     = "${var.project_name}-rg"
  location = var.location
}
output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}
