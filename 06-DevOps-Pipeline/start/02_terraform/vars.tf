
# FRAGILE: the DevOps template sets all TFVars as environment variables, Terraform is case-sensitive, and so all these must be upper-case

# except this magic one which is lower-case for some reason
variable "tags" {
  type    = map(string)
  default = {}
}

variable "ENV_NAME" {
  type        = string
  description = "The environment name: dev, qa, prod, etc"
}

variable "AWS_REGION" {
  type        = string
  description = "The AWS region to deploy this project"
  default     = "us-west-2"
}

variable "LAMBDA_ZIP_FILE" {
  type        = string
  description = "The zip file containing the lambda function"
}
