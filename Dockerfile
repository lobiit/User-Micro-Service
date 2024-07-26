# userprofile_service/Dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 800

# Run database migrations
RUN python manage.py makemigrations
RUN python manage.py migrate

# Start the application
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "user_microservice.asgi:application"]
