
Overview
========
Kiloquad and Katalog endpoints will be used for providing object storage services within the Tachyonic framework. The original requirement is for consumption by Yoshii (telemetry) for storing time series data redundantly. 

Example topology:

.. code::

    Kiloquad1   Kiloquad2   Kiloquad3   Kiloquad4
       |           |           |           |
       =====================================
                   |           |
                Katalog1    Katalog2
                   |           |
                   =============
                     HA PROXY
                       ||
                      Yoshi

The katalog service will be repsonsible for indexing and proxying objects redundantly over 3 Kiloquads. 

Objects supported are:
    * Raw object (with mine_type header)
    * Timeseries - Object is stored and retrieved as pandas.

For time series data objects Panadas is used. Pandas is an open source, BSD-licensed library providing high-performance, easy-to-use data structures and data analysis tools for the Python programming language. https://pandas.pydata.org

Both Katalog and Kiloquad should understand the timeseries object types for the purpose of only selecting a range of data. This is to ensure that we do not download unnecessary amount of data for an object to display a graph for example.

API Flow:
       
.. code::

    Yoshi -> Katalog -> Kiloquad1
                   | -> Kiloquad2
                   | -> Kiloquad3

Authentication
--------------
    * Users will be created for each Katalog to access the Kiloquad.
    * A new role will be added storage and assigned to Katalog.
    * Yoshi for example would have a user to consume Katalog with storage role.

API Headers
-----------
For raw objects Content-Type header will be set on POST/GET with minetype of object. (optional)
Range header will be used to define a range in bytes to retrieve or location to patch.
X-Object-Type will be used to define 'raw' or 'timeseries' for data type. (default being 'raw'.


Kiloquad
========

Resources
---------
GET Request /v1/storage - Retrieve object with node values.
The node values will include initially property of available disk space.
This value will be used by Katalog to understand how much space a new node has.

GET Request /v1/object/{id} - Retrieve Object.

POST Request /v1/object - Upload Object.

DELETE Request /v1/object/{id} - Delete Object.

PATCH Request /v1/object/{id} - Append Object.

Abstraction
-----------

There will be 3 levels of abstraction on the API Calls.

    1. The object parser to be used based on X-Object-Type header.
    2. The storage engine to use. 
    3. The actual API Responder.

Use the get_class function from luxon.utils.imports for using an object parser or storage engine.

The storage engine class must be defined under [storage] in settings.ini for Kiloquad endpoint.

Initially only one storage will be included to store files in path defined in settings.ini file in section [storage].

Storing data
------------
When data/object is updated it must make a copy of the data to to a temporary file then sync it once upload is complete by moving file over original. The temporary file name could be uuid.tmp. (uuid being the object id).

Files should be locked using file system function in python to ensure they cannot be open untill the above action of moving temporary over original is complete.


Katalog
=======
Katalog will have API(s) for defining new Kiloquads and their respective API(s) and proxy and index objects. It will be need to distribute objects over 3 Kiloquads in round-robin fashion tracking which objects are on which kiloquad. In round-robin fashion files will also be retrieved from a Kiloquad. 

Katalog will track which objects are completed when uploading/updating so necessary proxy calls can be directed to latest object.

Resources
---------
GET Request /v1/storage - Retrieve object with node values.
The node values will include initially property of available disk space.
This value will be used by Katalog to understand how much space a new node has.

GET Request /v1/object/folder/folder/obj - Retrieve Object.

POST Request /v1/object/folder/folder/obj - Upload Object.

DELETE Request /v1/object/folder/folder/obj - Delete Object.

PATCH Request /v1/object/folder/folder/obj - Append Object.

Database
--------
For speed its better to not use data models to query the database, however are used and built to maintain and build the initial database.

