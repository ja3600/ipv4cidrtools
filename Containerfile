#Comment these out if deploy via Openshift web
FROM python:3.13-slim
LABEL version="2.0"
LABEL app="ipv4cidrtools"
LABEL maintainer="https://github.com/ja3600/ipv4cidrtools.git"

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app app/
COPY wsgi.py .
COPY entrypoint.sh .

# Expose Flask default port
EXPOSE 5000

# Use a non-root user for security (optional)
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Set environment variables for Flask
ENV FLASK_APP=wsgi.py
ENV FLASK_DEBUG=0

# Set the host for Flask development server; remove if using Gunicorn or another WSGI server
ENV FLASK_RUN_HOST=0.0.0.0

# Start the Flask app
CMD ["flask", "run"]

