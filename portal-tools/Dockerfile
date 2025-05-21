# === Builder Stage ===
FROM python:3.11-slim AS builder

WORKDIR /app

# Install uv and other build tools (optional: gcc, libffi-dev if needed)
RUN pip install uv

# Copy and compile dependencies
COPY pyproject.toml uv.lock ./
RUN uv pip compile pyproject.toml > requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# === Final Image ===
FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy app source code
COPY --from=builder /app /app

# Expose port
EXPOSE 8080

# Launch command
CMD ["gunicorn", "-b", "0.0.0.0:8080", "portal_tools.app:app"]