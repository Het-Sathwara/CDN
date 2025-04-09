#!/bin/bash

# Start replica servers
echo "Starting replica servers..."
python3 replicaserver.py 33000 &
python3 replicaserver.py 33001 &
python3 replicaserver.py 33002 &

# Wait a moment for replica servers to initialize
sleep 2

# Start load balancer
echo "Starting load balancer..."
python3 loadbalancer.py &

# Wait a moment for load balancer to initialize
sleep 2

# Start HTTP server for client page
echo "Starting HTTP server for client page..."
python3 -m http.server 8000 &

echo "All servers started!"
echo "Access the client page at: http://localhost:8000/client.html" 