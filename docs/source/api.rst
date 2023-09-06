API
===

This page is currently under construction. Feel free to visit this page at a later time!

Authentication and Administration Endpoints
-------------------------------------------

.. http:post:: /api/v3/projects/

    Create a registration request. This request needs to be accepted by an administrator before the user can sign in.

    **Example request**:

    .. tabs::

        .. code-tab:: bash

            $ curl \
              -X POST \
              -H "Authorization: Token <token>" https://readthedocs.org/api/v3/projects/ \
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


Public Endpoints
----------------