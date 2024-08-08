# Deployment Guide

## Introduction

!!! warning "Attention"

    We would like to kindly remind you that, as the owner of your instance, you are responsible for setting up your own backup and recovery strategy. While we do not provide any warranties with the hosted instance, we hope you understand that hosting your own Scorpion instance means you are solely responsible for any potential data losses.

### Overview
This deployment guide provides a comprehensive walkthrough for setting up and deploying Scorpion. It is designed to ensure that both novice and experienced developers can successfully deploy Scorpion without encountering common pitfalls. The guide covers everything from preparing the deployment environment, including infrastructure and network configurations, to the actual deployment process itself, including pre-deployment checks, deployment steps, and post-deployment verification. Additionally, it offers guidance on troubleshooting common issues, maintaining the application, and updating it over time. Whether you're deploying a new Scorpion instance or maintaining an existing one, this guide aims to streamline the deployment process and minimize downtime.

### Prerequisites

To deploy Scorpion, you must have the following prerequisites met:

__Software:__

- **Docker:** Version 27.0.3 or later is required. Ensure Docker is installed and running correctly on your system.
- **Docker Compose:** Version 2.28.1 or later is needed. Docker Compose should also be installed and configured properly alongside Docker.

__Hardware Specifications:__

- **Operating System:** Tested on Ubuntu 22.04 LTS.
- **CPU:** A minimum of 14 CPUs is recommended for optimal performance.
- **RAM:** At least 32 GB of RAM is required to handle the application's workload efficiently.
- **Storage:** A base storage of 50 GB is necessary, with additional storage allocated for database contents as needed.

__Network Configurations:__

- **Ports:** The application requires ports 80 and 443 to be open and available for HTTP and HTTPS traffic respectively. Ensure these ports are not blocked by any firewalls or security groups.

## Service Deployment Process

### Pre-deployment Checks

Before deploying Scorpion, you need to clone the repository.

=== "HTTPS"
    ```bash
    git clone https://github.com/IPK-BIT/scorpion.git
    ```

=== "SSH"
    ```bash
    git@github.com:IPK-BIT/scorpion.git
    ```

=== "Github CLI"
    ```bash
    gh repo clone IPK-BIT/scorpion
    ```

### Deployment Steps

!!! danger "Attention"

    This is a pretty manual deployment process, since we're really focusing on developing the central hosted instance. But if you're set on hosting your own instance, you'll need to make a few changes to the source code, especially for the base URLs. We'll be providing proper deployment tooling as time allows, so keep an eye out for that!

**Step 1: Prepare Environment Variables**

Ensure that `.env` files are present in both `/api/app/` and `/webui/`. These files should contain all necessary environment variables for the application to function correctly.

**Step 2: Deploy API Component**

Navigate to the `api/` directory. Adjust the path for the database storages according to your setup and execute the following command to start the API component using Docker Compose:

```bash 
cd ./api && docker-compose up -d
```

This command starts the API server as well as the neo4j and influxDB databases in detached mode.

**Step 3: Deploy WebUI Component**

Change the current directory to `webui/` and run the following command to deploy the WebUI component:

```bash
cd ../webui && docker-compose up -d
```

This command starts the web interface and the proxy in detached mode.

**Step 4: Add Resources to API Component**

Create and add the `jwt-key.crt` and `jwt-key.pem` files to the `api/app/` directory. These files are crucial for secure communication within the application.

**Step 5: Configure the Proxy**

Open `localhost:81` in your web browser to access the Nginx Proxy Manager web interface. Create a new Proxy Host for `INTERNAL_IP:3000` to your domain name and add SSL certificates as necessary. Configure the custom locations as follows:

- `/aai` -> `INTERNAL_IP:8000`
- `/api/v1` -> `INTERNAL_IP:8000`
- `/docs` -> `INTERNAL_IP:8000`

**Step 6: Update Neo4j Password**

Access the Neo4j Web UI at `localhost:7474`, change the default, store it in the `.env` file located in `api/app/`, and proceed to add the KPI, Categories, and Service Providers to the Neo4j graph. The specific queries for adding these elements will be provided separately.

**Step 7: Set Up InfluxDB Bucket and Token**

Open the InfluxDB Web UI at `localhost:8086` and create a bucket named `kpis`. Generate an API token and add this token to the `.env` file located in `api/app/`.

### Post-deployment Verification

After completing the deployment steps, verify that all services are running correctly by checking the status of the containers managed by Docker Compose. Access each service through its designated port (e.g., `localhost:3000` for the web interface) and confirm that they are accessible and functioning as expected.

## Maintenance and Updates

### Updating the Application
To update the Scorpion application after it has been deployed, follow these steps:

1. **Pull Latest Changes**: Navigate to the root directory and pull the latest changes.
2. **Update Dependencies**: Navigate to the `./api` and `./webui` directories and rebuild the Docker containers to apply the updates. Use the following commands:
```bash
cd ./api && docker-compose up -d --build 
cd ../webui && docker-compose up -d --build
```
3. **Verify Updates**: After rebuilding the containers, verify that the application is functioning correctly by accessing the web interface and API endpoints.

### Backup and Recovery Procedures
Regular backups are essential for maintaining the integrity of your application data. Follow these procedures for backup and recovery:

1. **Backup Data**:

    - **Database**: Schedule regular backups of your Neo4j and InfluxDB databases. For Neo4j, use the `neo4j-admin dump` command, and for InfluxDB, use the `influxd backup` command.
    - **Configuration Files**: Ensure that configuration files, especially `.env` files and SSL certificates, are backed up regularly.

2. **Recovery Procedure**:

    - In case of failure, restore the database backups using the `neo4j-admin load` command for Neo4j and the `influxd restore` command for InfluxDB.
    - Replace any lost configuration files with their backups and restart the application containers using Docker Compose.

## Troubleshooting

Here will be a list of already answered questions on issues that occured while deploying Scorpion.
