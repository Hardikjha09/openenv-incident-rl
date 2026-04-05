FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r server/requirements.txt

# Set PYTHONPATH so our modules can find each other
ENV PYTHONPATH="/app:$PYTHONPATH"

# Expose the port
EXPOSE 8000

# Health check — judges ping this to verify your Space is alive
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Start the FastAPI server
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000"]