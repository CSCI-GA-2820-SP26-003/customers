#!/bin/bash
#
# These must be installed as a user and therefore need to be run
# after the container has been created.
#
echo "**********************************************************************"
echo "Setting up Docker user development environment..."
echo "**********************************************************************"

echo "Setting up insecure registry for cluster-registry:5000..."
sudo mkdir -p /etc/docker
sudo bash -c 'echo "{\"insecure-registries\": [\"cluster-registry:5000\"]}" > /etc/docker/daemon.json'

echo "Setting up cluster-registry in /etc/hosts..."
# Use a placeholder IP that will be updated after the cluster is created
# Run 'make registry-setup' after 'make cluster' to update the real IP
if ! grep -q "cluster-registry" /etc/hosts; then
    sudo bash -c "echo '127.0.0.1    cluster-registry' >> /etc/hosts"
fi

echo "Making git stop complaining about unsafe folders"
git config --global --add safe.directory /app

echo "**********************************************************************"
echo "Setup complete"
echo "**********************************************************************"
