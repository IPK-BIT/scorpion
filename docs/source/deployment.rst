Deployment
==========

This page is currently under construction. Feel free to visit it again at a later point to find more information.

Software Architecture
---------------------

Scorpion is a system developed to monitor KPIs for services of the NFDi4Biodiversity Service Catalog. In our context, KPIs are mostly focussed on usage of a service (e.g. Number of Unique Users). The KPI measurements are submitted in a push approach, so that every service provider is responsible for submitting their KPI measurements on a monthly basis to Scorpion. The system itself is structured in several layers:

.. figure:: images/scorpion-architecture.png
    :alt: Architecture

    System architecture of Scorpion.

Storage Layer
+++++++++++++

The base layer of Scorpion is responsible for storage. It is composed of three databases each responsible for its own distinct domain. The UserDB uses a SQLite3 database and manages user registration and role assignement. Its implementation is kept minimal to later allow a simple integration of IAM solutions. The Meta Store is run by a Neo4j instance, which manages the KPI to category as well as service to category or resp. KPI relations. In addition it keeps track of service provider memberships. The KPI Store is an InfluxDB instance run to store KPI measurements of the services in a time series. It uses the Neo4j instance as a safeguard to only allow the storage of measurements of valid service and KPI combinations.
As all databases have their distinct domain, synchronization tasks can be kept to a minimum. Communication between the databases is realized through the API.

API Layer
+++++++++

The API Layer comprises a REST API implemented using FastAPI. It is kept fairly simple and is organized into three modules. The first module is responsible for authentication and authorization and will in the future partially be replaced with an IAM solution. The second module contains all public endpoints that are provided to users to retrieve data from Scorpion programmatically. Thirdly, there is a private endpoints module comprising all endpoints related to administration tasks or features that are not available to access programmatically such as service registration. The endpoints are secured by the usage of JWT. In addition, administrative endpoints require the administrator role.

GUI Layer
+++++++++

On top of the Storage and API Layer, is a GUI Layer, which is realized by a Web Interface implemented with Svelte. It serves as a low-barrier entrypoint to submit the KPI measurements and request service provider memberships without technical knowledge on how to use a REST API. It is also used for all administration purposes as well as service registrations. Lastly, it can be used to visualize KPI measurements and download them as figures. 

RDC Integration
---------------

Scorpion is part of the RDC management and governance layer. It collects and visualizes KPIs useful for the review process. Scorpion offers a REST API as well as a form in the GUI to submit KPIs for a service on a monthly basis. Additionally, it offers basic visualisations of the measurements to help the NFDI4Biodiversity Service Review Committee to decide what measures need to be taken to ensure the service complies with our definition of quality.

.. figure:: images/rdc-integration.png
    :alt: RDC Integration

    Integration into the RDC.

Further information specific to the NFDI4Biodiversty instance can be found in the `KnowledgeBase <https://kb.gfbio.org/display/KB/Service+Monitoring%3A+Scorpion>`_.

Installation Guide
------------------

Here you will find further information about the necessary steps to set up your own Scorpion instance.