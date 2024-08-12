#!/bin/bash

# Update and install necessary packages
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y docker.io git

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Clone the GitHub repository
REPO_URL="https://github.com/mhtkmr74/TechAssignment.git"
REPO_DIR="TechAssignment"

if [ -d "$REPO_DIR" ]; then
  sudo rm -rf "$REPO_DIR"
fi

git clone $REPO_URL

# Navigate to the repository directory
cd "$REPO_DIR"

# Build the Docker image
sudo docker build -t tech-assignment .

# Run the Docker container
sudo docker run -d -p 8000:8000 tech-assignment

# Print the status of Docker container
sudo docker ps

# Setup security group rules (assuming EC2 instance)
# Replace with actual security group ID
SECURITY_GROUP_ID="your-security-group-id"

aws ec2 authorize-security-group-ingress --group-id $SECURITY_GROUP_ID --protocol tcp --port 8000 --cidr 0.0.0.0/0

# Optionally, add a health check to verify deployment
sleep 10
curl http://localhost:8000

echo "Deployment script completed."
