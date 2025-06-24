terraform {
  required_version = ">= 0.13"

  required_providers {
    # No external providers required for this module
    # It only uses null_resource which is built into Terraform
  }
}