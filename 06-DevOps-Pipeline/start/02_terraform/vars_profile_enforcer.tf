## ==================================================
## Safety to ensure only executed in personnal AWS account
##
## INSTRUCTIONS:
## * Usage: export TF_VAR_LOCAL_AWS_PROFILE="${AWS_PROFILE}"
## * Remark: Do NOT add to var.tf nor input.tfvars. This variable
## is to be used strictly from the OS environemnt variable context
##
variable "LOCAL_AWS_PROFILE" {
  type        = string
  description = "Are we using the right AWS profile? Please abort and set TF_VAR_LOCAL_AWS_PROFILE env var"

  validation {
    condition     = can(regex("^(confoo)$", var.LOCAL_AWS_PROFILE))
    error_message = "Not a valid ZIP file. Expected extension .zip for input file."
  }
}