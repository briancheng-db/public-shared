locals {
  # Build the command based on whether to run after deploy
  deploy_command = "databricks bundle validate -t $target && databricks bundle deploy -t $target"
  run_command    = var.is_run_after_deploy ? "&& databricks bundle run ${var.job} -t $target --no-wait" : ""
}

resource "null_resource" "dab_bundle" {
  provisioner "local-exec" {
    command = <<EOT
set -e
echo "Starting DAB bundle execution for target: ${var.target}"

export target=${var.target}
${local.deploy_command} ${local.run_command}

echo "DAB bundle execution completed for target: ${var.target}"
EOT
    interpreter = ["bash", "-c"]
    working_dir = var.working_dir
  }

  # For testing, create or replace the resource every time
  triggers = {
    always_run = timestamp()
  }
}