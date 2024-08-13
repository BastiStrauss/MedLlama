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
if command -v xdg-open > /dev/null; then
  xdg-open http://localhost:8501
elif command -v open > /dev/null; then
  open http://localhost:8501
elif command -v start > /dev/null; then
  start http://localhost:8501
else
  echo "Could not detect the web browser command to open the URL. Please open it manually: http://localhost:8501"
fi