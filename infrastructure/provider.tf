provider "aws" {
  region = var.aws_region
}


# Centraliza o arquivo de controle do terraform
terraform {
  backend "s3" {
    bucket = "nefesh-terraform-state"
    key    = "nefesh-state/terraform.tfstate"
    region = "us-east-2"
  }
}