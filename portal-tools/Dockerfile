# Use official Python base image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install uv (a fast Python package manager)
RUN pip install uv

# Copy dependency files first for caching
COPY pyproject.toml uv.lock /app/

# Compile a pip requirements file from your uv.lock and install dependencies
RUN uv pip compile pyproject.toml > requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expose port (customize if different)
EXPOSE 5000

# Run the app (adjust if you use app.py or uvicorn, etc.)
CMD ["gunicorn", "-b", "0.0.0.0:8080", "portal_tools.app:app"]
