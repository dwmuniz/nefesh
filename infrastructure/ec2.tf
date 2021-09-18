# Imagem Ubuntu
data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
  owners = ["054118696149"]
}


# Instância EC2
resource "aws_instance" "airflow" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t2.medium"
  key_name                    = var.key_pair_name
  associate_public_ip_address = true
  security_groups             = [aws_security_group.airflow_sg.id]
  subnet_id                   = var.airflow_subnet_id

  provisioner "file" {
    source      = "~/install.sh"
    destination = "/tmp/install.sh"
  }
  # Change permissions on bash script and execute from ec2-user.
  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/install.sh",
      "sudo install.sh",
    ]
  }
  tags = {
    PROJECT   = "NEFESH",
    AUTHOR    = "Daniela Muniz"
  }
}

# Security group to allow acces to instance
resource "aws_security_group" "airflow_sg" {
  name        = "airflow_sg"
  description = "Allow traffic on port 8080 for airflow"
  vpc_id      = var.vpc_id

  ingress {
    description      = "TLS from VPC"
    from_port        = 8080
    to_port          = 8080
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  ingress {
    description      = "TLS from VPC"
    from_port        = 5555
    to_port          = 5555
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  ingress {
    description      = "TLS from VPC"
    from_port        = 22
    to_port          = 22
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    PROJECT   = "NEFESH",
    AUTHOR    = "Daniela Muniz"
  }
}
