## REFERENCE: https://spacelift.io/blog/terraform-aws-s3-bucket
## REFERENCE: https://spacelift.io/blog/aws-iam-roles
## REFERENCE: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket


#DONE, create on March 16th at 4pm EST
resource "aws_s3_bucket" "confoo_tf_state" {
  bucket = "gh-actions-tf-confoo-cmos"

  tags = {
    Name        = "My bucket"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket_versioning" "versioning_example" {
  bucket = aws_s3_bucket.confoo_tf_state.id
  versioning_configuration {
    status = "Enabled"
  }
}



/* **************************************************

variable "name" { default = "dynamic-aws-creds-operator" }
variable "region" { default = "us-west-2" }
variable "path" { default = "../vault-admin-workspace/terraform.tfstate" }
variable "ttl" { default = "1" }
 
terraform {
 backend "local" {
   path = "terraform.tfstate"
 }
}
 
data "terraform_remote_state" "admin" {
 backend = "local"
 
 config = {
   path = var.path
 }
}
 
data "vault_aws_access_credentials" "creds" {
 backend = data.terraform_remote_state.admin.outputs.backend
 role    = data.terraform_remote_state.admin.outputs.role
}
 
provider "aws" {
 region     = var.region
 access_key = data.vault_aws_access_credentials.creds.access_key
 secret_key = data.vault_aws_access_credentials.creds.secret_key
}
 
resource "aws_s3_bucket" "spacelift-test1-s3" {
   bucket = "spacelift-test1-s3"
   acl = "private"  
}

resource "aws_s3_bucket_object" "object1" {
 for_each = fileset("uploads/", "*")
 bucket = aws_s3_bucket.spacelift-test1-s3.id
 key = each.value
 source = "uploads/${each.value}"
}

resource "aws_s3_bucket_public_access_block" "app" {
bucket = aws_s3_bucket.spacelift-test1-s3.id
block_public_acls       = true
block_public_policy     = true
ignore_public_acls      = true
restrict_public_buckets = true
}
************************************************** */