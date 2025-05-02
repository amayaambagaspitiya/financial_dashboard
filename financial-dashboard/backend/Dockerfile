# Use an official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install torch==2.4.1 --index-url https://download.pytorch.org/whl/cpu
RUN pip install -r requirements.txt

# Copy the rest of the backend code
COPY . .

# Run the app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
