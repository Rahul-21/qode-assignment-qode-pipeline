FROM python:3.11-bookworm

WORKDIR /app

COPY requirements.txt .

# Install Chromium + ChromeDriver + dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
      chromium chromium-driver fonts-liberation \
      libnss3 libgconf-2-4 libxi6 libxcursor1 libxrandr2 libxss1 libxtst6 \
      libatk1.0-0 libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip setuptools wheel --trusted-host pypi.org --trusted-host files.pythonhosted.org \
    && pip install selenium==4.21.0 --trusted-host pypi.org --trusted-host files.pythonhosted.org \
    && pip install textblob==0.17.1 --trusted-host pypi.org --trusted-host files.pythonhosted.org \
    && pip install --no-cache-dir -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org

COPY src/ ./src
COPY data/ ./data
COPY logs/ ./logs

CMD ["python", "src/main.py"]
