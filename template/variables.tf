variable "target" {
  description = "The target environment for Databricks bundle (dev, stg, prod)"
  type        = string
  validation {
    condition     = contains(["dev", "stg", "prod"], var.target)
    error_message = "Target environment must be one of: dev, stg, prod."
  }
}

variable "job" {
  description = "The name of the Databricks bundle job to run"
  type        = string
}


variable "working_dir" {
  description = "The working directory for the Databricks bundle commands"
  type        = string
}

variable "is_run_after_deploy" {
  description = "Whether to run the job after deployment (true) or just deploy (false)"
  type        = bool
  default     = true
}

variable "env_file_prefix" {
  description = "Prefix for environment files (e.g., 'env' for env_dev_stg.sh, env_prod.sh)"
  type        = string
  default     = "env"
}
