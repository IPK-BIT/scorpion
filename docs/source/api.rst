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

    .. note::
        The registration process, including the acceptance of the request, must be finished prior to being able to sign in.

    **Example requests**:

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

.. _publicendpoints:

Public Endpoints
----------------