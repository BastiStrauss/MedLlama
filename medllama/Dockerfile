# Use the official Python image as a base
FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu \
    transformers==4.33.0 \
    streamlit==1.25.0 \
    Pillow==9.4.0

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . .

# Expose the port that Streamlit will run on
EXPOSE 8501

# Set the entrypoint to run the Streamlit app
CMD ["streamlit", "run", "medllama/ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
