terraform {
  backend "azurerm" {
    use_azuread_auth     = true
    tenant_id = var.azure_sp_tenant_id
    client_id = var.azure_sp_client_id
    client_secret = var.azure_sp_client_secret
  }
}