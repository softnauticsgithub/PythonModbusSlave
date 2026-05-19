# Modbus Slave Application Guide

This guide explains how to create and use a Docker image for the Python-based Modbus Slave application.

The application includes:

- Modbus TCP Server
- MQTT Subscriber/Publisher
- YAML-based register mapping
- Event handling logic

---

## 1. Project Structure

Recommended structure:

```text
modbus-slave-app/
├── app/
│   ├── StartTCPServer.py
│   ├── mqttEventHandler.py
│   ├── EventBus.py
│   ├── logger_config.py
│   └── ...
├── registers.yml
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 2. Build Docker Image

Run this command from the project root:

```bash
docker build -t modbus-slave-app .
```

Verify the image:

```bash
docker images
```

---

## 3. Run Docker Container

### Option A: MQTT broker running on the host machine

On Linux/Raspberry Pi, use:

```bash
docker run -d \
  --name modbus_slave \
  --add-host=host.docker.internal:host-gateway \
  -p 5020:5020 \
  -e MQTT_BROKER=host.docker.internal \
  -e MQTT_PORT=1883 \
  modbus-slave-app
```

### Option B: MQTT broker running on another machine

Use the broker IP address:

```bash
docker run -d \
  --name modbus_slave \
  -p 5020:5020 \
  -e MQTT_BROKER=192.168.1.20 \
  -e MQTT_PORT=1883 \
  modbus-slave-app
```

---

## 4. Environment Variables

| Variable | Description | Example |
|---|---|---|
| `MQTT_BROKER` | MQTT broker host/IP | `host.docker.internal` |
| `MQTT_PORT` | MQTT broker port | `1883` |

---

## 5. Check Container Status

```bash
docker ps
```

If the container stopped:

```bash
docker ps -a
```

---

## 6. View Logs

Show logs:

```bash
docker logs modbus_slave
```

Follow live logs:

```bash
docker logs -f modbus_slave
```

Recommended command:

```bash
docker logs -f -t --tail 100 modbus_slave
```

---


## 7. Stop and Remove Container

Stop:

```bash
docker stop modbus_slave
```

Remove:

```bash
docker rm modbus_slave
```

Rebuild and rerun:

```bash
docker build -t modbus-slave-app .

docker run -d \
  --name modbus_slave \
  --add-host=host.docker.internal:host-gateway \
  -p 5020:5020 \
  -e MQTT_BROKER=host.docker.internal \
  modbus-slave-app
```

---

## 8. Export Image for Sharing

Save image as a tar file:

```bash
docker save modbus-slave-app > modbus-slave-app.tar
```

Load image on another system:

```bash
docker load < modbus-slave-app.tar
```

Run it:

```bash
docker run -d \
  --name modbus_slave \
  -p 5020:5020 \
  -e MQTT_BROKER=<broker-ip> \
  -e MQTT_PORT=1883 \
  modbus-slave-app
```

---

## 9. Recommended Runtime Flow

```text
Docker Container Starts
        ↓
Load registers.yml
        ↓
Start MQTT Client
        ↓
Subscribe to device/modbus/in
        ↓
Start Modbus TCP Server on 5020
        ↓
Receive MQTT event
        ↓
Update Modbus registers
        ↓
Publish response/event to device/modbus/out
```

---

## 10. Useful Commands Summary

```bash
# Build image
docker build -t modbus-slave-app .

# Run container
docker run -d --name modbus_slave --add-host=host.docker.internal:host-gateway -p 5020:5020 -e MQTT_BROKER=host.docker.internal modbus-slave-app

# View logs
docker logs -f modbus_slave

# Stop container
docker stop modbus_slave

# Remove container
docker rm modbus_slave

# Export image
docker save modbus-slave-app > modbus-slave-app.tar

# Import image
docker load < modbus-slave-app.tar
```
