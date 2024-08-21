# Deployment Guide

## Introduction

!!! warning "Attention"

    We would like to kindly remind you that, as the owner of your instance, you are responsible for setting up your own backup and recovery strategy. While we do not provide any warranties with the hosted instance, we hope you understand that hosting your own Scorpion instance means you are solely responsible for any potential data losses.

### Overview
This deployment guide provides a comprehensive walkthrough for setting up and deploying Scorpion. It is designed to ensure that both novice and experienced developers can successfully deploy Scorpion without encountering common pitfalls. The guide covers everything from preparing the deployment environment, including infrastructure and network configurations, to the actual deployment process itself, including pre-deployment checks, deployment steps, and post-deployment verification. Additionally, it offers guidance on troubleshooting common issues, maintaining the application, and updating it over time. Whether you're deploying a new Scorpion instance or maintaining an existing one, this guide aims to streamline the deployment process and minimize downtime.

### Prerequisites

To deploy Scorpion, you must have the following prerequisites met:

__Software:__

- **Ansible:** 2.17.3 or later is required. Ensure Ansible is installed and running correctly on your control node.
- **Docker:** Version 27.0.3 or later is required. Ensure Docker is installed and running correctly on your hosting system.
- **Docker Compose:** Version 2.28.1 or later is needed. Docker Compose should also be installed and configured properly alongside Docker.

__Hardware Specifications:__

- **Operating System:** Tested on Ubuntu 22.04 LTS.
- **CPU:** A minimum of 14 CPUs is recommended for optimal performance.
- **RAM:** At least 32 GB of RAM is required to handle the application's workload efficiently.
- **Storage:** A base storage of 50 GB is necessary, with additional storage allocated for database contents as needed.

__Network Configurations:__

- **Ports:** The application requires ports `80` and `443` to be open and available for HTTP and HTTPS traffic respectively. Ensure these ports are not blocked by any firewalls or security groups. For the web UI port `3000` is used by the docker container, for the API `8000`. The docker containers for the databases use ports `8086`, `7474` and `7687`. 

## Service Deployment Process

### Pre-deployment Checks

Before starting the deployment process. Download and extract the latest release on your control node.
Ensure that the control node has access to the managed node(s). Adapt the `ansible.cfg` as necessary.

<!-- === "HTTPS"
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
    ``` -->

### Deployment Steps

**Step 1: Prepare Playbook Execution**

The ansible playbook comes along templates, files and variable environments. Familiarize yourself with them and adapt as necessary. The environments are preconfigured but empty and need to be filled according to your set up. 

**Step 2: Deploy Scorpion Components**

When you have configured everything, you can start the deployment by executing:

```bash
ansible-playbook -i environments/<ENV>/hosts playbook.yml
```

Don't forget to change `<ENV>` to the environment you want to deploy.

**Step 3: Proxy setup**

While depending on your setup, ensure that the reverse proxy is set up correctly and redirects traffic to the correct hosts and ports.

- API Port: `8000`
- Web UI Port: `3000`

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
