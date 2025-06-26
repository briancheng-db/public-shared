terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.1"
    }
    databricks = {
      source  = "databricks/databricks"
      version = "~>1.83.0"
    }
    azuread = {
      source  = "hashicorp/azuread"
    }
  }
}


provider "databricks" {
  host                        = var.databricks_host
  azure_workspace_resource_id = var.azure_ws_resource_id
  azure_client_id             = var.azure_sp_client_id
  azure_client_secret         = var.azure_sp_client_secret
  azure_tenant_id             = var.azure_sp_tenant_id
}
