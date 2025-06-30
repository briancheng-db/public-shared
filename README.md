# Databricks Asset Bundle (DAB) Sample Project

This project demonstrates how to use Databricks Asset Bundles (DAB) to deploy and manage Databricks resources across different environments using Azure DevOps pipelines.

## Overview

- **Databricks Asset Bundles (DAB)** for resource management
- **Azure DevOps Pipelines** for automated deployment
- **Service Principal Authentication** for secure deployments

## Prerequisites

1. **Databricks CLI**: Install from [Databricks CLI Documentation](https://docs.databricks.com/dev-tools/cli/databricks-cli.html)
2. **Azure DevOps**: Access to Azure DevOps with appropriate permissions
3. **Azure Service Principal**: With permissions to access your Databricks workspace

## Project Structure

```
dab_sample/
├── conf/                          # Environment configurations
│   ├── dev.yml                   # Development environment
│   ├── stg.yml                   # Staging environment
│   └── prod.yml                  # Production environment
├── notebooks/                     # Databricks notebooks
│   └── table_select.ipynb        # Sample notebook
├── resources/                     # DAB resource definitions
│   └── dab_table_select_job.yml  # Job configuration
└── databricks.yml                # Main bundle configuration

azure-pipelines.yml               # Azure DevOps pipeline configuration
```


## Azure DevOps Pipeline

### Pipeline Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `is_run_after_deploy` | Run job after deployment | `'false'` |
| `job_name` | Name of the job to run | `'dab_table_select_job'` |
| `working_directory` | Working directory path | `'$(System.DefaultWorkingDirectory)/dab_sample'` |
| `target` | DAB deployment target | `'dev'` |

### Pipeline Steps

1. **Install Azure CLI**: Installs Azure CLI for authentication
2. **Install Required Packages**: Installs unzip, curl, and dependencies
3. **Install Databricks CLI**: Installs Databricks CLI
4. **Azure Authentication**: Logs in using service principal
5. **Bundle Validation**: Validates DAB configuration
6. **Bundle Deployment**: Deploys to target environment
7. **Job Execution** (Optional): Runs specified job after deployment

### Required Variables

Create variable group `scb-demo` in Azure DevOps:

| Variable | Description |
|----------|-------------|
| `azure_sp_client_id` | Service principal client ID |
| `azure_sp_client_secret` | Service principal client secret |
| `azure_sp_tenant_id` | Azure tenant ID |
| `azure_ws_resource_id` | Databricks workspace resource ID |

### Commands
```bash
# Validate bundle
databricks bundle validate -t dev

# Deploy to development
databricks bundle deploy -t dev

# Run job
databricks bundle run dab_table_select_job -t dev

# Check status
databricks bundle status -t dev
```

## Deployment Modes

- **Development Mode**: Resources prefixed with `[dev username]`, schedules paused
- **Production Mode**: Resources deployed as-is, schedules active


## Additional Resources

- [Databricks Asset Bundles Documentation](https://docs.databricks.com/dev-tools/bundles/index.html)
- [Databricks CLI Documentation](https://docs.databricks.com/dev-tools/cli/databricks-cli.html)
- [Azure DevOps Pipelines](https://docs.microsoft.com/en-us/azure/devops/pipelines/)
- [Service Principal Authentication](https://docs.databricks.com/dev-tools/bundles/authentication.html)
