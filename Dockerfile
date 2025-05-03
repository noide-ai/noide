FROM python:3.12-slim

# Install Git and other dependencies
RUN apt-get update && apt-get install -y git && apt-get clean

# Set working directory
WORKDIR /app

# Copy your code
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "./src/main.py"]