FROM python:3.11-slim

WORKDIR /app

# Copy everything from the project root
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r server/requirements.txt

# Set PYTHONPATH so imports work
ENV PYTHONPATH="/app:$PYTHONPATH"

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "8000"]