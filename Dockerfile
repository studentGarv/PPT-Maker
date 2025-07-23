# Dockerfile for PPT Maker
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.ai/install.sh | sh

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt requirements_web.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements_web.txt

# Copy application files
COPY *.py ./
COPY config.py ./

# Expose port for web interface
EXPOSE 7860

# Create startup script
RUN echo '#!/bin/bash\n\
ollama serve &\n\
sleep 10\n\
ollama pull llama3\n\
python web_app.py\n\
' > start.sh && chmod +x start.sh

# Run the application
CMD ["./start.sh"]
