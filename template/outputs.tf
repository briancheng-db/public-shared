output "resource_id" {
  description = "The ID of the created null_resource"
  value       = null_resource.dab_bundle.id
}

output "target" {
  description = "The target environment that was used"
  value       = var.target
}

output "job" {
  description = "The job name that was executed"
  value       = "${var.working_dir}::${var.job}"
}

output "working_dir" {
  description = "The working directory that DAB was used"
  value       = var.working_dir
}
