terraform {
  required_providers {


    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.83"
    }
  }

  backend "s3" {
  }
}

provider "aws" {
  region = "us-west-2"
}
