FROM python:3.10-slim

# ----------------------------------------
# Environment
# ----------------------------------------

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ----------------------------------------
# Working Directory
# ----------------------------------------

WORKDIR /app

# ----------------------------------------
# Install Dependencies
# ----------------------------------------

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# ----------------------------------------
# Copy Application
# ----------------------------------------

COPY . .

# ----------------------------------------
# Expose Modbus TCP Port
# ----------------------------------------

EXPOSE 5020

# ----------------------------------------
# Start Application
# ----------------------------------------

CMD ["python", "app/StartTCPServer.py"]