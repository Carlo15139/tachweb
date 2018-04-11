Infinitystone: Login and Scope Change
=====================================

Infinitystone uses Tokens for Authentication and Authorization. Every single request has to be accompanied with an HTTP Header called `X-Auth-Token`.

When logging in for the first time, one is dropped into the Global scope, and provided with a Global Token. It is also possible to work inside a Domain or Tenant. In order to do that, a scoped Token is required.

The global token is used to obtain the scoped token.

This is a basic tutorial that will walk you through logging in and changing scope using Infinitystone's REST API. To try this out, Infinitystone needs to be installed on a running webserver. If you do not already have Infinitystone Installed and running, refer to the Introduciton Tutorial_. You will need some way of sending HTTP requests to the API such as Postman_ or curl.

.. _Postman: https://www.getpostman.com/

.. _Tutorial: http://www.tachyonic.org/rst/introduction

1. Login
--------

In this tutorial we will log into the Infinitystone running on our local webserver at 
**http://127.0.0.1/api**

Let's send Infinitystone a simple HTTP request to test it.

| Create a request with GET as the method to **http://127.0.0.1/api/v1/token** 
| The return data should be an empty Json object:

.. code-block:: json

    {}

Now let's actually log in as the root user.
Perform an HTTP POST to **http://127.0.0.1/api/v1/token** with the default username and password given as a JSON object in the *Body* section of the request.

POST data:

.. code-block:: json

	{
		"username": "root",
		"password": "password"
	}

Return Data:

.. code-block:: json

	{
	    "domain": null,
	    "tenant_id": null,
	    "creation": "2018/03/19 14:22:12",
	    "expire": "2018/03/19 15:22:12",
	    "username": "root",
	    "token": "f1rgNZgrla4lHqKGEa0ZPnaDA73EpnleAEiknDWwxYOZOuJaFHK7cf7IaI7wTrnqm01/OjO5k3P0khcs8ybIKWJGJB1/tZOSKG5fzBFE6WSnS3cvvhunmjkEHdGa426Vy2HYi+LE4MF33DwLwXofg1IRVJozrd4sT1NLsWLHMTKYYQkjzdvutjWdaNGLyRBeL/ffXJBYHHltBvXTgbRt50QhlJP5m6WUxfiE2IxkziqOFcb6nxTvMc4i3w6v5UEZelamCP+oZMPCEVkeI1UavdKdJ1FEL+6+S/crIgcJVnyatCvYdXwT3xdHoGGHjvQWA7OtVKJGCfaovqY2+9X5kw==!!!!ewogICAgImRvbWFpbiI6IG51bGwsCiAgICAidXNlcm5hbWUiOiAicm9vdCIsCiAgICAiY3JlYXRpb24iOiAiMjAxOC8wMy8xOSAxNDoyMjoxMiIsCiAgICAiZXhwaXJlIjogIjIwMTgvMDMvMTkgMTU6MjI6MTIiLAogICAgInRlbmFudF9pZCI6IG51bGwsCiAgICAidXNlcl9pZCI6ICIwMDAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDAiLAogICAgInJvbGVzIjogWwogICAgICAgICJSb290IgogICAgXQp9",
	    "user_id": "00000000-0000-0000-0000-000000000000",
	    "roles": [
	        "Root"
	    ]
	}

As you can see this creates a global token (as can be seen by the *null* values for tenant_id and domain) with a number of attributes, including a user_id, an encoded token and a tenant_id.

The value of `token` is needed to authenticate future transactions, used as the value in the **X-Auth-Token** Header. Be aware that the token expires after one hour, after that a new one will have to be generated.


2. Change the Scope
-------------------

To change the scope to a Tenant for example, all we need to do is change the *tenant_id* in the Token of our root user to the *id* of our tenant.

To do this we create an HTTP PATCH request again with the **X-Auth-Token** header set to the global token string and a `tenant_id` in the body.

HEADER data:

.. code-block:: text

    X-Auth-Token = f1rgNZgrla4lHqKGEa0ZPnaDA73EpnleAEiknDWwxYOZOuJaFHK7cf7IaI7wTrnqm01/OjO5k3P0khcs8ybIKWJGJB1/tZOSKG5fzBFE6WSnS3cvvhunmjkEHdGa426Vy2HYi+LE4MF33DwLwXofg1IRVJozrd4sT1NLsWLHMTKYYQkjzdvutjWdaNGLyRBeL/ffXJBYHHltBvXTgbRt50QhlJP5m6WUxfiE2IxkziqOFcb6nxTvMc4i3w6v5UEZelamCP+oZMPCEVkeI1UavdKdJ1FEL+6+S/crIgcJVnyatCvYdXwT3xdHoGGHjvQWA7OtVKJGCfaovqY2+9X5kw==!!!!ewogICAgImRvbWFpbiI6IG51bGwsCiAgICAidXNlcm5hbWUiOiAicm9vdCIsCiAgICAiY3JlYXRpb24iOiAiMjAxOC8wMy8xOSAxNDoyMjoxMiIsCiAgICAiZXhwaXJlIjogIjIwMTgvMDMvMTkgMTU6MjI6MTIiLAogICAgInRlbmFudF9pZCI6IG51bGwsCiAgICAidXNlcl9pZCI6ICIwMDAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDAiLAogICAgInJvbGVzIjogWwogICAgICAgICJSb290IgogICAgXQp9

PATCH data:

.. code-block:: json
	
	{
		"tenant_id": "a3817fb3-ea93-4429-8107-880b592cab64"
	}

Return Data:

.. code-block:: json

	{
	    "user_id": "00000000-0000-0000-0000-000000000000",
	    "creation": "2018/03/19 14:46:25",
	    "expire": "2018/03/19 15:22:12",
	    "domain": null,
	    "roles": [
	        "Root"
	    ],
	    "token": "MOqygk/7oK1T4VARYjngO9HgApw/2JOifVIa0kdkQsquUmzVQS3vB2XQ605RK1oImos+NcmY5LsY57KMv9cwgUmExdG4ujRtmsbIbqJ3Hx6usFC1K014G8cT08TYj2rlWkyd3Qic2WTeZgwayZ2pwpMK6GbKGAqf1dQWRtkKFeEXZfMuxJMWJHRb7nr42506oGV+3eSHM10tRfJ2GY1r6hP8mZBCC/ZeCkdF1VRo+oQ9xyfSh9FWQSWeu4BJIJ5gKkbroENclLFOC9fTLzBARm0Mg68aS08wy4g62saw/kYwblvQo4j7J4N4s9nizLZOxRRzXQLN7paZvo0VkoiyUA==!!!!ewogICAgInVzZXJfaWQiOiAiMDAwMDAwMDAtMDAwMC0wMDAwLTAwMDAtMDAwMDAwMDAwMDAwIiwKICAgICJjcmVhdGlvbiI6ICIyMDE4LzAzLzE5IDE0OjQ2OjI1IiwKICAgICJleHBpcmUiOiAiMjAxOC8wMy8xOSAxNToyMjoxMiIsCiAgICAiZG9tYWluIjogbnVsbCwKICAgICJyb2xlcyI6IFsKICAgICAgICAiUm9vdCIKICAgIF0sCiAgICAidGVuYW50X2lkIjogImEzODE3ZmIzLWVhOTMtNDQyOS04MTA3LTg4MGI1OTJjYWI2NCIsCiAgICAidXNlcm5hbWUiOiAicm9vdCIKfQ==",
	    "tenant_id": "a3817fb3-ea93-4429-8107-880b592cab64",
	    "username": "root"
	}

The scope has now been successfuly changed, as can be seen from the value for the *tenant_id* in this scoped token. To work inside the scope of this Tenant, use this scoped token as the value for the **X-Auth-Token** header, and use this tenant_id as the value for the **X-Tenant-Id** Header. Tokens scoped inside a domain behaves similarly, where the PATCH data should include a value for *domain*, and the subsequent requests should include the same value in the **X-Domain** Header.

.. (@vuader) This part should move to the Infinitystone UserGuide
.. 2. Creating a Tenant
    --------------------

    To create a new tenant we need to do a an HTTP POST to **http://127.0.0.1/api/v1/tenant** as the root user, using the token that we generated in the last step.

    To do this create a POST request and give it a header with the key: *X-Auth-Token* and the token string as the value.

    .. code-block:: text

        X-Auth-Token: f1rgNZgrla4lHqKGEa0ZPnaDA73EpnleAEiknDWwxYOZOuJaFHK7cf7IaI7wTrnqm01/OjO5k3P0khcs8ybIKWJGJB1/tZOSKG5fzBFE6WSnS3cvvhunmjkEHdGa426Vy2HYi+LE4MF33DwLwXofg1IRVJozrd4sT1NLsWLHMTKYYQkjzdvutjWdaNGLyRBeL/ffXJBYHHltBvXTgbRt50QhlJP5m6WUxfiE2IxkziqOFcb6nxTvMc4i3w6v5UEZelamCP+oZMPCEVkeI1UavdKdJ1FEL+6+S/crIgcJVnyatCvYdXwT3xdHoGGHjvQWA7OtVKJGCfaovqY2+9X5kw==!!!!ewogICAgImRvbWFpbiI6IG51bGwsCiAgICAidXNlcm5hbWUiOiAicm9vdCIsCiAgICAiY3JlYXRpb24iOiAiMjAxOC8wMy8xOSAxNDoyMjoxMiIsCiAgICAiZXhwaXJlIjogIjIwMTgvMDMvMTkgMTU6MjI6MTIiLAogICAgInRlbmFudF9pZCI6IG51bGwsCiAgICAidXNlcl9pZCI6ICIwMDAwMDAwMC0wMDAwLTAwMDAtMDAwMC0wMDAwMDAwMDAwMDAiLAogICAgInJvbGVzIjogWwogICAgICAgICJSb290IgogICAgXQp9

    POST data:

    .. code-block:: json

        {
            "name": "Test Tenant"
        }

    Return Data:

    .. code-block:: json

        {
            "id": "a3817fb3-ea93-4429-8107-880b592cab64",
            "creation_time": "2018/03/19 14:32:21",
            "domain": null,
            "name": "Test Tenant",
            "enabled": null,
            "tenant_id": null
        }

