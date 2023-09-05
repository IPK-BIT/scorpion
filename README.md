# Scorpion
> :warning: **The project is in active development and changes can be made without further notice!**
## About
Scorpion is a Dashboard that collects and visualizes Key Performance Indicators (KPI) for services. KPIs are measurements we agreed upon to monitor how well a service is performing. Based on trends over a year this will give insights into what measures to take. Scorpion is the tool that is used to collect the results of all services in the Service Monitoring and generate plots and overviews for the review processs.

## Installation
The project is composed of two parts. First the API with connection to three databases. You can start the API by running 
```
docker compose up
```
inside the ```/api``` directory. The second part is the (optional) Web UI, which can be started by runnning 
```
npm install
docker compose up
```
inside the ```/webui``` directory. 

## Documentation
Documentation of the context of use inside of NFDI4Biodiversity can be found here: TBP
Documentation of the software can be found by building deploying ```docs/_build/html/index.html```.
