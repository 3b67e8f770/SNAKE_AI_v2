# 1 Python slim
FROM python:3.13-slim

# 2. Pygame install (screen & sound)
RUN apt-get update && apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libfreetype6-dev \
    libportmidi-dev \
    libavformat-dev \
    libswscale-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. WORKDIR 
WORKDIR /app

# 4. Lib list
COPY requirements.txt .
RUN pip install --no-cache-dir \
    --trusted-host pypi.org \
    --trusted-host files.pythonhosted.org \
    -r requirements.txt

# 5. copy app to the container 
COPY src/ ./src/

# 6. what to run
CMD ["python", "src/main.py"]