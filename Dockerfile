FROM python:3.10-slim

# Install Chromium (the open source version of Chrome) and its driver
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your scripts
COPY . .

# Run the web server to satisfy Render's port requirement
CMD sh -c "gunicorn --bind 0.0.0.0:${PORT:-10000} --timeout 0 app:app"
