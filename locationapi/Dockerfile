# day8/locationapi/Dockerfile
FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code
ENV PYTHONPATH=/code
# Install system deps if needed (uncomment if you need them)
# RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . /code/

# Expose port (container port)
EXPOSE 9000

# Run the FastAPI app using uvicorn
# If your main file is not main.py, change "main:app" accordingly
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000"]
