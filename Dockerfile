FROM python:3.12-slim

# Create working directory
WORKDIR /app

# Install dependencies
COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip pipenv && \
    pipenv install --system --deploy

# Copy application code
COPY wsgi.py .
COPY service/ ./service/

# Expose port
EXPOSE 8080

# Run the service
CMD ["gunicorn", "--bind=0.0.0.0:8080", "--log-level=info", "wsgi:app"]
