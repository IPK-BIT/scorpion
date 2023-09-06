API
===

This page is currently under construction. Feel free to visit this page at a later time!

Authentication and Authorization Endpoints
-------------------------------------------

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

    Sign in to the system. The returned JSON Web Token (JWT) must be added as a Bearer token in the ```Authorization``` header to all subsequent calls, in order to be authenticated and access to features can be authorized.

    **Example requests**:

    .. tabs::

        .. code-tab:: bash

            $ curl \
              -X POST \
              -H "Authorization: Basic ZGVtbzp0b3BzZWNyZXRwYXNzd29yZG5vb25lY2FuZ3Vlc3M=" https://example.com/aai/login \
              -H "Content-Type: application/json" \
              -d @body.json

        .. code-tab:: python

            import requests
            import json
            HEADERS = {'Authorization': 'Basic ZGVtbzp0b3BzZWNyZXRwYXNzd29yZG5vb25lY2FuZ3Vlc3M='}
            URL = 'https://example.com/aai/login'
            response = requests.post(
                URL
                headers=HEADERS,
            )
            print(response.json())

    .. note::
        The registration process, including the acceptance of the request, must be finished prior to being able to sign in.

    **Example responses**:
    
    .. sourcecode:: json
        {
          "detail": "login successful",
          "token": "{TOKEN}"
        }

Public Endpoints
----------------