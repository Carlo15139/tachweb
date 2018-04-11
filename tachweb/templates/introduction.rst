Tutorial
========

.. contents:: This tutorial will walk through a basic deployment of Photonic in an Ubuntu environment, using Luxon to install Photonic and it's two dependencies: Infinitystone and Psychokinetic


Deploying on Ubuntu 16.04 LTS
==================================

Prerequisites
----------------------------------

Preparing the Operating System for all required dependencies and ensuring the environment are configured to run the applications. 

.. code:: bash
    
    $ apt-get update
    $ apt-get --assume-yes install apache2
    $ apt-get --assume-yes install apache2-dev
    $ apt-get --assume-yes install apache2-utils
    $ apt-get --assume-yes install libcurl4-openssl-dev libssl-dev
    $ apt-get --assume-yes install python3
    $ apt-get --assume-yes install python3-dev
    $ apt-get --assume-yes install python3-pip
    $ apt-get --assume-yes install git
    $ apt-get --assume-yes install sqlite3
    $ apt-get clean 

Additonal python modules
--------------------------------

We will need to host Python web applications in our Apache Server so to facilitate that let's install the mod_wsgi module.

.. code:: bash 

    $ pip3 install mod-wsgi

Attach the wsgi module to Apache's available modules

.. code:: bash

    $ echo 'LoadModule wsgi_module "/usr/local/lib/python3.5/dist-packages/mod_wsgi/server/mod_wsgi-py35.cpython-35m-x86_64-linux-gnu.so"' > /etc/apache2/mods-available/wsgi.load

If you have trouble with persmissions try:

.. code:: bash
    
    $ echo 'LoadModule wsgi_module "/usr/local/lib/python3.5/dist-packages/mod_wsgi/server/mod_wsgi-py35.cpython-35m-x86_64-linux-gnu.so"' | sudo tee /etc/apache2/mods-available/wsgi.load

Enable the wsgi module for Apache.

# Throw an error, might be that the environment not properly set, or check top python3.5 ... not sure if python3.6 would be the default install, (Make note, how to check python version... inform reader perhaps)


.. code:: bash
    
    $ a2enmod wsgi

Now let's clone all the relevant scource code. This tutorial will clone it into the root directory by default.

.. code:: bash

    $ cd /root
    $ git clone -b development https://github.com/TachyonicProject/luxon.git
    $ git clone -b development https://github.com/TachyonicProject/psychokinetic.git
    $ git clone -b development https://github.com/TachyonicProject/photonic.git
    $ git clone -b development https://github.com/TachyonicProject/infinitystone.git

Next we'll install the modules from the source code with pip3 so that they can be used in python

.. code:: bash

    $ cd /root/luxon
    $ pip3 install -r requirements.txt
    $ pip3 install .
    $ cd /root/psychokinetic
    $ pip3 install .
    $ cd /root/photonic
    $ pip3 install .
    $ cd /root/infinitystone
    $ pip3 install .


Now it's time to deploy Photonic and Infinitystone in our Apache webserver 
We'll navigate to /var/www and make directories Infinitystone and Photonic


.. code:: bash

    $ cd /var/www
    $ mkdir infinitystone 
    $ mkdir photonic

First let's deal with Infinitystone:

We will use luxon to install Infinitystone with the -i command

.. code:: bash
    
    $ luxon -i infinitystone infinitystone
 
Luxon can also set up the database for Infinitystone by using the -d command

.. code:: bash

    $ luxon -d infinitystone

Set the user and group to www-data

.. code:: bash

    $ chown -R www-data:www-data infinitystone

And set the permissions for the database file

.. code:: bash

    $ chmod 770 infinitystone/sqlite3.db

We need to rename the database to tachyon

.. code:: bash
    
    $ mv infinitystone/sqlite3.db infinitystone/tachyon

The Infinitystone installation needs a copy of the settings.ini and policy.json files which. So we will create symbolic links to the original files to get around this. 

.. code:: bash

    $ ln -s /root/infinitystone/infinitystone/settings.ini infinitystone/settings.ini
    $ ln -s /root/infinitystone/infinitystone/policy.json infinitystone/policy.json

Now let's repeat the process for Photonic:

Install with Luxon.

.. code:: bash
    
    $ luxon -i photonic photonic

The Photonic installation creates a file: static incorrectly, we need to remove and replace with a symbolic link to the file in the source code 

.. code:: bash
    
    $ rm -rf photonic/static
    $ ln -s /root/photonic/photonic/static/ photonic/static

And as before link to the settings.ini/policy.json files

.. code:: bash

    $ ln -s /root/photonic/photonic/settings.ini photonic/settings.ini
    $ ln -s /root/photonic/photonic/policy.json photonic/policy.json

Both modules need tmp directories to store session data

.. code:: bash

    $ mkdir infinitystone/tmp
    $ mkdir photonic/tmp

Set the user:group for those to www-data as well

.. code:: bash 

    $ chown -R www-data:www-data infinitystone/tmp
    $ chown -R www-data:www-data photonic/tmp

Both modules need a pki certificate. We'll create it in Infinitystone

.. code:: bash

    $ cd /var/www/infinitystone
    $ openssl req  -nodes -new -x509  -keyout token.key -out token.cert -subj "/C=ZA/ST= /L= /O= /OU= /CN= "

And we'll just link it to Photonic

.. code:: bash

    $ ln -s ../infinitystone/token.cert ../photonic/token.cert
    
We will give Photonic's static dirctory to the webserver so that we can interface with Tachyonic via a browser. Again with a symbolic link

.. code:: bash

    $ ln -s /root/photonic/photonic/static/ /var/www/html/static


Finally download a sample apache .config file, give it to our web server and reload Apache for this new file to take effect


.. code:: bash


    $ cd /etc/apache2/sites-enabled/
    $ wget https://raw.githubusercontent.com/TachyonicProject/photonic/development/photonic/resources/000-default.conf
    $ sudo service apache2 reload
    
At this point we should have a working instilation of Photonic. To view it browse to http://127.0.0.1/ui and log in with 

| username: *root*
| password: *password*


Running Luxon Framework
=======================================

Due to wsgi deployment capabilities, the framework can be deployed on various different ways, leaving the user to decide their own preferred. 

In this tutorial we would be covering running luxon as a standalone application followed by deploying it on an Apache2.

Running as Standalone
---------------------------------------

 luxon -s <directory>


Running by making use of Mod_WSGI module
-----------------------------------------

 apache2 configurations, restart and project initializations, etc etc... 












