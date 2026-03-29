# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY ./app ./app

# Expose port
EXPOSE 8000

# Command to run the app with Uvicorn
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "9441"]