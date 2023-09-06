API
===

The available REST API is structured into two modules. The first is in regards of :ref:`aai` and is responsible for user management. The second module lists all :ref:`publicendpoints`. Those enpoints are mostly ```GET``` calls to receive information about the current data, as well as one ```POST``` endpoint to submit KPI measurements for a service.

.. _aai:

Authentication and Authorization
--------------------------------

.. http:post:: /aai/register

    Create a registration request. This request needs to be accepted by an administrator before the user can sign in.

    **Example request**:

    .. tabs::

        .. code-tab:: bash

            $ curl \
              -X POST \
              https://example.com/aai/register \
              -H "Content-Type: application/json" \
              -d @body.json

        .. code-tab:: python

            import requests
            import json
            URL = 'https://example.com/aai/register'
            data = json.load(open('body.json', 'rb'))
            response = requests.post(
                URL,
                json=data,
            )
            print(response.json())

    The content of ``body.json`` is like,

    .. sourcecode:: json

        {
            "user_name": "demo",
            "email": "demo@example.com",
            "password": "topsecretpasswordnoonecanguess"
        }

    **Example response**:
    
    .. sourcecode:: json

        {
          "user_name": "demo",
          "email": "demo@example.com",
          "user_id": "2a2fe33c-7bcf-4e0c-a50a-3f4a6c2079cd"
        }

.. http:post:: /aai/login

    Sign in to the system. The returned JSON Web Token (JWT) must be added as a Bearer token in the ```Authorization``` header to all subsequent calls in order to be authenticated and access to features can be authorized.

    .. warning::
        The registration process, including the acceptance of the request, must be finished prior to being able to sign in.

    **Example requests**:

    .. tip:: 
        The login information are encoded as Base64 in the ```Authorization``` header.

    .. tabs::

        .. code-tab:: bash

            $ curl -X 'POST' \
              'http://example.com/aai/login' \
              -H 'accept: application/json' \
              -H 'Authorization: Basic ZGVtbzp0b3BzZWNyZXRwYXNzd29yZG5vb25lY2FuZ3Vlc3M' \
              -d ''

        .. code-tab:: python

            import requests
            import json
            HEADERS = {'Authorization': 'Basic ZGVtbzp0b3BzZWNyZXRwYXNzd29yZG5vb25lY2FuZ3Vlc3M'}
            URL = 'https://example.com/aai/login'
            response = requests.post(
                URL
                headers=HEADERS,
            )
            print(response.json())

    
    **Example responses**:
    
    .. sourcecode:: json

        {
          "detail": "login successful",
          "token": "{TOKEN}"
        }

.. http:post:: /aai/logout

    Logout from Scorpion. 

    **Example requests**:

    .. tabs::

        .. code-tab:: bash

            $ curl -X 'POST' \
              'http://example.com/aai/logout' \
              -H 'accept: application/json' \
              -d ''

        .. code-tab:: python

            import requests
            import json
            URL = 'https://example.com/aai/logout'
            response = requests.post(
                URL
            )
            print(response.json())

    
    **Example responses**:
    
    .. sourcecode:: json

        {
          "detail": "logout successful",
          "token": null
        }

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
                             Allowed values are abbreviations that can be looked up with :ref:`getproviders`
    
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

.. _getproviders:

.. http:get:: /api/v1/providers
    
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