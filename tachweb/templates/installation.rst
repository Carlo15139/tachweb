Deploying Photonic on Ubuntu 16.04 LTS
======================================

This tutorial will walk through a basic deployment of Photonic in an Ubuntu environment, using Luxon to install Photonic and it's two dependencies: Infinitystone and Psychokinetic.
We will launch an Apache WebServer and install these componets on it. We will be able to use the Psychokinetic API through direct calls or via the Photonic gui which will be displayed in our browser. 

Prerequisites
-----------------------

Check your python installation, Tachyonic needs python 3.5 or 3.6

.. code:: bash

    $ python3 --version
        Python 3.5.2

We will be using pip3 to install Tachyonic's modules. It should already be installed in the Python 3 binaries

.. code:: bash

        $ pip3 --version 
            pip 8.1.1 from /usr/lib/python3/dist-packages (python 3.5)

Now let's install some prerequisites

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
    $ apt-get --assume-yes install libapache2-mod-wsgi-py3
    $ apt-get clean 

| At this point you should have all the required dependencies and a running Apache webserver.
| Navigate to the local host *https://127.0.0.1* to see the **Apache2 Ubuntu Default Page**

Installation
---------------------

Currently the only way to install the modules is to compile from the source code, luckily this is very easy.

The relevant source code is all hosted on github, let's clone it.
This tutorial will clone it into the root directory by default.

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

We will use Luxon to install Infinitystone with the **-i** command

.. code:: bash
    
    $ luxon -i infinitystone infinitystone
 
Luxon can also set up the database for Infinitystone by using the **-d** command

.. code:: bash

    $ luxon -d infinitystone

Set the user and group, we'll call them each "www-data"

.. code:: bash

    $ chown -R www-data:www-data infinitystone

And set the permissions for the database file

.. code:: bash

    $ chmod 770 infinitystone/sqlite3.db

We need to rename the database to "tachyon"

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

The Photonic installation creates a file: *static* incorrectly, we need to remove and replace with a symbolic link to the file in the source code 

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

Set the user:group for those to "www-data" as well

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
    
We will give Photonic's *static* dirctory to the webserver so that we can interface with Tachyonic via a browser. Again with a symbolic link

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
