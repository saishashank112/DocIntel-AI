FROM python:3.10-slim

# Install system packages required for compilation/extraction
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /app

# Copy dependency definition and install packages
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy all source files
COPY . .

# Expose Streamlit's default port
EXPOSE 8501

# Add standard Streamlit healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Command to run the application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
