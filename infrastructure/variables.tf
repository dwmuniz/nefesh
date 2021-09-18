variable "aws_region" {
  default = "us-east-2"
}

variable "key_pair_name" {
  default = "pipeline_key_pair"
}

variable "airflow_subnet_id" {
  default = "subnet-c19e50aa"
}

variable "vpc_id" {
  default = "vpc-f72b8c9c"
}
