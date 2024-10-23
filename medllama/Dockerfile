# Use Python 3.11 as base
FROM python:3.11

# Set environment variables for Poetry
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    POETRY_VERSION=1.7.1

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . .

# Install dependencies using Poetry
RUN poetry install 

# Expose the port that Streamlit will run on
EXPOSE 8501

# Set the entrypoint to run the Streamlit app
CMD ["streamlit", "run", "medllama/ui.py"]
