provider "aws" {
  region = "us-east-1" # You can change this to your closest AWS region
}

# 1. Create a Security Group to allow web traffic into your server
resource "aws_security_group" "api_sg" {
  name        = "ml-api-security-group"
  description = "Allow inbound HTTP and SSH traffic"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Anyone can access the API endpoint
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Allows you to SSH into the machine if needed
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"] # Allows the server to talk to the internet
  }
}

# 2. Define the Virtual Server (EC2)
resource "aws_instance" "ml_server" {
  ami           = "ami-0c7217cdde317cfec" # Standard Ubuntu 22.04 LTS AMI in us-east-1
  instance_type = "t2.micro"             # Free-tier eligible server size

  vpc_security_group_ids = [aws_security_group.api_sg.id]

  # Startup Script: Run automatically when the machine boots up
  user_data = <<-EOF
              #!/bin/bash
              sudo apt-get update -y
              sudo apt-get install -y docker.io
              sudo systemctl start docker
              sudo systemctl enable docker
              
              # Pull and run your container from Docker Hub (Replace with your username/image)
              # For demonstration purposes, you can build it locally, but here is how IaC fetches it:
              # sudo docker run -d -p 80:80 your_dockerhub_username/ml-api:latest
              EOF

  tags = {
    Name = "MLOps-Production-API"
  }
}

# 3. Output the final IP address of your new server to the terminal screen
output "server_public_ip" {
  value       = aws_instance.ml_server.public_ip
  description = "The public IP address of your live deployed ML API server."
}
