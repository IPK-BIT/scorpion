API
===

This page is currently under construction. Feel free to visit this page at a later time!

Authentication and Administration Endpoints
-------------------------------------------

.. http:post:: /aai/register
   :noindex:
   
     Register as a user to the Scorpion. This endpoints adds a request for registration to the system. An administrator has to accept the request before the user can sign in.
   
.. important::
   The user_name and email must be unique within the system. Choosing a name or email already in use the request will be denied automatically.

**Example Request**

.. sourcecode:: bash
  
    curl -X POST https://example.com/aai/register

**Example Response**

.. sourcecode:: json

   {
      "user_name": "demo",
      "email": "demo [at] example dot com",
      "user_id": "40b61ae9-215e-47ff-92e0-0f066db5f7ba"
   }

Public Endpoints
----------------