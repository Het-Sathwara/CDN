#!/bin/bash

echo "Stopping all servers..."

# Kill all Python processes running our servers
pkill -f "python3.*loadbalancer.py"
pkill -f "python3.*replicaserver.py"
pkill -f "python3.*http.server"

echo "All servers stopped!" 