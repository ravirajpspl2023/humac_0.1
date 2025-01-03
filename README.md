# HumacGateway

## Overview
This project involves monitoring and controlling an HPDC (High Pressure Die Casting) machine using a Raspberry Pi and optocoupler. The data is collected and published to an MQTT broker for further analysis and monitoring, with support for offline connectivity and local data storage.

## Configuration
Provide the necessary configuration details in `common_configuration_file_sheet.csv`. This includes Modbus and GPIO pins configuration like parameter names, Modbus registers, or GPIO pin numbers.

## Details

### Project Structure
The project works in two distinct parts:

1. **Data Collection:**
   - Check `GPIOpins.py`: This module collects data from GPIO pins and stores it in shared memory.

2. **Data Delivery:**
   - Check `MqttBroker.py`: This module checks the network connectivity and publishes data to the MQTT server. If the network is unavailable, it stores the data locally. Once the network is available, it publishes the data to the server and deletes it from local storage.

## RUN

### Requirements
Ensure Docker is installed on your Raspberry Pi. If it is not installed, refer to the [official Docker website](https://www.docker.com/get-started) for installation instructions.

### Start the Project
Run the following Docker command to start the project:

```bash
   sudo docker compose up -d


