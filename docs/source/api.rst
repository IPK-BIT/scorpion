API
===

The available REST API is structured into two modules. The first is in regards of :ref:`aai` and is responsible for user management. The second module lists all :ref:`publicendpoints`. Those enpoints are mostly ```GET``` calls to receive information about the current data, as well as one ```POST``` endpoint to submit KPI measurements for a service.

.. _aai:

Authentication and Authorization
--------------------------------

.. http:get:: /aai/details

    Retrieve details of a user. Those details are username, email, membership for service providers, and whether the user is an administrator. 

    .. note:: 

        The information for which user the details are requested are provided through the JWT Token send via the ```Authorization``` Header.

    **Example request**:

    .. tabs::

        .. code-tab:: bash

            $ curl -X 'GET' \
              'http://example.com/aai/details' \
              -H 'accept: application/json' \
              -H 'Authorization: Bearer {TOKEN}'

        .. code-tab:: python

            import requests
            URL = 'http://example.com/aai/details'
            TOKEN = '<token>'
            HEADERS = {'Authorization': f'Bearer {TOKEN}'}
            response = requests.get(URL, headers=HEADERS)
            print(response.json())

    **Example response**:

    .. sourcecode:: json

        {
          "user_name": "demo",
          "email": "demo@example.com",
          "is_admin": false,
          "providers": [
              "IPK"
          ]
        }

.. http:post:: /aai/requests/membership

    Request a membership to a service provider. This membership is required to register new services to Scorpion and to submit KPI measurements for services of this provider. 
    
    :query string providers: Comma-seperated list of the abbreviations of the service providers one is requesting membership for.
                             Allowed values are abbreviations that can be looked up with ```GET /api/v1/providers```
    
    **Example requests**:

    .. tabs::

        .. code-tab:: bash

            $ curl -X 'POST' \
              'http://example.com/aai/requests/membership?providers=IPK' \
              -H 'accept: application/json' \
              -H 'Authorization: Bearer <TOKEN>' \
              -d ''

        .. code-tab:: python

            import requests
            import json
            URL = 'https://example.com/aai/logout'
            TOKEN = '<token>'
            HEADERS = {'Authorization': f'Bearer {TOKEN}'}
            response = requests.post(
                URL,
                headers=HEADERS
            )
            print(response.json())

    
    **Example responses**:
    
    .. sourcecode:: json

        {
          "id": "c775d812-0e8f-4933-9c03-7179a693593c",
          "mail": "demo@example.com",
          "username": "demo",
          "provider": "IPK"
        }
                          

.. _publicendpoints:

Public Endpoints
----------------

.. http:get:: /api/v1/providers
    
    List all providers registered to the system. The list includes names and abbreviations of the service providers.

    :query integer page: Pagination parameter to specify the requested page. Default value is 0.
    :query integer pageSize: Pagination parameter to specify the requested page size. Default value is 100.
    :query boolean is_member: Query parameter to enable filter the providers by those that the signed in user is member to. Default value is `false`.
    
    .. note:: 

        The information for which user the providers are filtered by is provided through the JWT Token send via the ```Authorization``` Header.

    **Example request**:

    .. tabs::

        .. code-tab:: bash

            $ curl -X 'GET' \
              'http://example.com/api/v1/providers' \
              -H 'accept: application/json' \
              -H 'Authorization: Bearer {TOKEN}'

        .. code-tab:: python

            import requests
            URL = 'http://example.com/api/v1/providers'
            TOKEN = '<token>'
            HEADERS = {'Authorization': f'Bearer {TOKEN}'}
            response = requests.get(URL, headers=HEADERS)
            print(response.json())

    **Example response**:

    .. sourcecode:: json

        {
          "metadata": {
            "currentPage": 0,
            "pageSize": 100,
            "totalPages": 1,
            "totalCount": 1
          },
          "result": [
            {
              "abbreviation": "IPK",
              "name": "Leibniz Insitut für Pflanzengenetik und Kulturpflanzenforschung Gatersleben"
            }
          ]
        }

.. http:get:: /api/v1/categories

    List all categories registered with the system. 
    
    :query integer page: Pagination parameter to specify the requested page. Default value is 0.
    :query integer pageSize: Pagination parameter to specify the requested page size. Default value is 100.
    
    **Example request**:

    .. tabs::

        .. code-tab:: bash

            $ curl -X 'GET' \
              'http://example.com/api/v1/categories' \
              -H 'accept: application/json' \
              -H 'Authorization: Bearer {TOKEN}'

        .. code-tab:: python

            import requests
            URL = 'http://example.com/api/v1/categories'
            TOKEN = '<token>'
            HEADERS = {'Authorization': f'Bearer {TOKEN}'}
            response = requests.get(URL, headers=HEADERS)
            print(response.json())

    **Example response**:

    .. sourcecode:: json

        {
          "metadata": {
              "currentPage": 0,
              "pageSize": 100,
              "totalPages": 1,
              "totalCount": 7
          },
          "result": [
            {
              "name": "Databases"
            },{
              "name": "Workflows"
            },{
              "name": "Tools"
            },{
              "name": "Webapplications"
            },{
              "name": "Libraries"
            },{
              "name": "Supports"
            },{
              "name": "Trainings"
            }
          ]
        }

.. http:get:: /api/v1/indicators
    
    List all Key Performance Indicators (KPIs) that are registered with the system. The list includes the necessities for the different categories. And whether the KPI is selected for a optionally filtered service.

    :query integer page: Pagination parameter to specify the requested page. Default value is 0.
    :query integer pageSize: Pagination parameter to specify the requested page size. Default value is 100.
    :query string category: Specify the category to filter the KPIs for.
    :query string service: Specify the service abbreviation to filter the KPIs for being selected by a specific service. This parameter overwrites the category query parameter.
    
    **Example request**:

    .. tabs::

        .. code-tab:: bash

            $ curl -X 'GET' \
              'http://example.com/api/v1/indicators' \
              -H 'accept: application/json' \
              -H 'Authorization: Bearer {TOKEN}'

        .. code-tab:: python

            import requests
            URL = 'http://example.com/api/v1/indicators'
            TOKEN = '<token>'
            HEADERS = {'Authorization': f'Bearer {TOKEN}'}
            response = requests.get(URL, headers=HEADERS)
            print(response.json())

    **Example response**:

    .. sourcecode:: json

        {
          "metadata": {
              "currentPage": 0,
              "pageSize": 100,
              "totalPages": 1,
              "totalCount": 7
          },
          "result": [
            {
              "name": "Actions",
              "description": "Number of actions performed (page views, downloads, searches, outlinks).",
              "categories": [
                  {
                  "name": "Databases",
                  "necessity": null
                  }
              ],
              "selected": false
            }
          ]
        }

.. http:get:: /api/v1/services
    
    List all services registered with the system.

    :query integer page: Pagination parameter to specify the requested page. Default value is 0.
    :query integer pageSize: Pagination parameter to specify the requested page size. Default value is 100.
    :query string provider: Specify the provider abbreviation to filter the services for.
    :query string service: Specify the service abbreviation to query for a specific service.
    
    **Example request**:

    .. tabs::

        .. code-tab:: bash

            $ curl -X 'GET' \
              'http://example.com/api/v1/services' \
              -H 'accept: application/json' \
              -H 'Authorization: Bearer {TOKEN}'

        .. code-tab:: python

            import requests
            URL = 'http://example.com/api/v1/services'
            TOKEN = '<token>'
            HEADERS = {'Authorization': f'Bearer {TOKEN}'}
            response = requests.get(URL, headers=HEADERS)
            print(response.json())

    **Example response**:

    .. sourcecode:: json

        {
          "metadata": {
              "currentPage": 0,
              "pageSize": 100,
              "totalPages": 1,
              "totalCount": 7
          },
          "result": [
            {
              "abbreviation": "TEST",
              "name": "TESTSERVICE",
              "category": "Workflows",
              "provider": "IPK"
            }
          ]
        }

.. http:get:: /api/v1/measurements
    
    Retrieve all KPI measurements for a service. The result set is filterable by additional parameters. The pagination is with respect to the date.
    
    :query string service: Mandatory parameter to specify the service for which the measurements should be retrieved.
    :query string start: Mandatory parameter to specify the start date of the date range. The date is formatted in ```YYYY-MM-DDTHH:MM:SSZ```
    :query string stop: Mandatory parameter to specify the end date of the date range.
    :query integer page: Pagination parameter to specify the requested page. Default value is 0.
    :query integer pageSize: Pagination parameter to specify the requested page size. Default value is 100.
    :query string indicators: Comma-seperated list of all indicators for which the measurements should be retrieved.
    
    **Example request**:

    .. tabs::

        .. code-tab:: bash

            $ curl -X 'GET' \
              'http://example.com/api/v1/measurements?service=TEST&start=2022-01-01T00%3A00%3A00Z&stop=2023-12-31T00%3A00%3A00Z' \
              -H 'accept: application/json' \
              -H 'Authorization: Bearer {TOKEN}'

        .. code-tab:: python

            import requests
            URL = 'http://example.com/api/v1/measurements?service=TEST&start=2022-01-01T00%3A00%3A00Z&stop=2023-12-31T00%3A00%3A00Z'
            TOKEN = '<token>'
            HEADERS = {'Authorization': f'Bearer {TOKEN}'}
            response = requests.get(URL, headers=HEADERS)
            print(response.json())

    **Example response**:

    .. sourcecode:: json

        {
          "metadata": {
            "currentPage": 0,
            "pageSize": 1,
            "totalPages": 9,
            "totalCount": 9
          },
          "result": [
            {
              "kpi": "Citations",
              "date": "2023-01-01 00:00:00+00:00",
              "value": 3,
              "comment": null
            },
            {
              "kpi": "Executions",
              "date": "2023-01-01 00:00:00+00:00",
              "value": 31,
              "comment": null
            },
            {
              "kpi": "Helpdesk Tickets",
              "date": "2023-01-01 00:00:00+00:00",
              "value": 5,
              "comment": null
            },
            {
              "kpi": "Projects",
              "date": "2023-01-01 00:00:00+00:00",
              "value": 2,
              "comment": null
            },
            {
              "kpi": "Storage Usage",
              "date": "2023-01-01 00:00:00+00:00",
              "value": 637,
              "comment": null
            },
            {
              "kpi": "Support Tickets",
              "date": "2023-01-01 00:00:00+00:00",
              "value": 3,
              "comment": null
            },
            {
              "kpi": "Users",
              "date": "2023-01-01 00:00:00+00:00",
              "value": 1,
              "comment": null
            }
          ]
        }

.. http:post:: /api/v1/measurements

    Submit KPI measurements for a service. Returns a list of all measurements that have been successfully stored.

    .. warning:: 

        In order to submit measurements to a service one must first request membership for a service provider. See ```POST /requests/membership``` for more details.
    
    :query string service: Mandatory parameter to specify the service for which the measurements should be retrieved.
    
    **Example request**:

    .. tabs::

        .. code-tab:: bash

            $ curl \
              -X POST \
              -H "Authorization: Bearer <TOKEN>" https://example.com/api/v1/measurements \
              -H "Content-Type: application/json" \
              -d @body.json

        .. code-tab:: python

            import requests
            import json
            URL = 'https://example.com/api/v1/measurements'
            TOKEN = '<token>'
            HEADERS = {'Authorization': f'Bearer {TOKEN}'}
            data = json.load(open('body.json', 'rb'))
            response = requests.post(
                URL,
                json=data,
                headers=HEADERS
            )
            print(response.json())

    The content of ``body.json`` is like,

    .. sourcecode:: json

        [
          {
            "kpi": "Executions",
            "date": "2023-09",
            "value": 42
          }
        ]

    **Example response**:
    
    .. sourcecode:: json

        [
          {
            "kpi": "Executions",
            "date": "2023-09",
            "value": 42
          }
        ]