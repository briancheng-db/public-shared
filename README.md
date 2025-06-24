# Databricks Asset Bundle (DAB) Sample Project

This project demonstrates how to use Databricks Asset Bundles (DAB) to deploy and manage Databricks resources via Terraform across different environments (development, staging, and production).


## Prerequisites

1. **Databricks CLI**: Install the Databricks CLI from [Databricks CLI Documentation](https://docs.databricks.com/dev-tools/cli/databricks-cli.html)

2. **Databricks Workspace Access**: You need access to a Databricks workspace with appropriate permissions


## Authentication Setup ([ref](https://learn.microsoft.com/en-gb/azure/databricks/dev-tools/bundles/authentication))
### Service Principal Authentication (Recommended for CI/CD)

For production deployments and CI/CD pipelines, use service principal authentication:

**Set Environment Variables**:
   ```bash
   export DATABRICKS_CLIENT_ID="your-service-principal-client-id"
   export DATABRICKS_CLIENT_SECRET="your-service-principal-client-secret"
   export DATABRICKS_HOST="https://your-workspace-url"
   ```


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
├── databricks.yml                # Main bundle configuration
└── README.md
```


## Terraform Deployment

This project includes a Terraform template that automates the deployment of Databricks Asset Bundles. The Terraform configuration uses a `null_resource` with `local-exec` provisioner to execute DAB commands.

### Terraform Structure

```
template/
├── main.tf              # Main Terraform configuration
├── variables.tf         # Input variables definition
├── outputs.tf           # Output values
└── versions.tf          # Terraform and provider versions

dev/westeurope/2178/
└── terraform.tfvars     # Environment-specific variables
```

### Terraform Variables

The following variables can be configured in your `terraform.tfvars` file:

| Variable | Description | Type | Default | Example |
|----------|-------------|------|---------|---------|
| `target` | Target environment (dev, stg, prod) | string | - | `"dev"` |
| `job` | Name of the DAB job to run | string | - | `"dab_table_select_job"` |
| `working_dir` | Path to the DAB project directory | string | - | `"../dab_sample"` |
| `is_run_after_deploy` | Whether to run job after deployment | bool | `true` | `true` |
| `env_file_prefix` | Prefix for environment files | string | `"env"` | `"env"` |

### Deployment Commands

#### 1. Initialize Terraform

Navigate to the template directory and initialize Terraform:

```bash
cd template
terraform init
```

#### 2. Plan Deployment

Review the deployment plan before applying:

```bash
# For development environment
terraform plan -var-file="../dev/westeurope/2178/terraform.tfvars"

```

#### 3. Apply Deployment

Deploy the DAB bundle using Terraform:

```bash
terraform apply -auto-approve plan.out

```


## Additional Resources

- [Databricks Asset Bundles Documentation](https://learn.microsoft.com/en-gb/azure/databricks/dev-tools/bundles/)
- [Databricks CLI Documentation](https://learn.microsoft.com/en-gb/azure/databricks/dev-tools/cli/)
- [Deployment Modes](https://learn.microsoft.com/en-gb/azure/databricks/dev-tools/bundles/deployment-modes)
- [Terraform null_resource](https://www.terraform.io/docs/providers/null/resource.html)
