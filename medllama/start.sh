#!/bin/bash

# Start Docker Compose in detached mode
docker-compose up --build -d

# Wait for a few seconds to allow the application to start
sleep 10

# Check if Streamlit is running and retry if not
while ! curl -s http://localhost:8501/ > /dev/null; do
  echo "Waiting for Streamlit to start..."
  sleep 2
done

# Open the web browser
xdg-open http://localhost:8501 || open http://localhost:8501 || start http://localhost:8501