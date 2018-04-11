
.. contents::

Overview
=========================================================

In the following tutorial we would be covering how we currently have deployed a Luxon Framework Lab Environment. The contents of this document have configurations, and acts as a walk through on how to deploy the Luxon Framework.

Please do not email any improvements and or any comments to the current deployment to, team@tachyonic.org.

Lab Environment
=========================================================

Tachyonic Team, configured and installed six Ubuntu 16.04.4 LTS servers.

These servers would be broken down as follow:

1.) HAProxy [HA] - 172.16.0.16

2.) Sql1    [S1] - 172.16.0.13

3,) Sql2    [S2] - 172.16.0.14

4.) Sql3    [S3] - 172.16.0.12

5.) Lab1    [L1] - 172.16.0.18

6.) Lab2    [L2] - 172.16.0.19

Please note the "[]" tags, it is used throughout the document to give clarity which steps to be run on which servers. 


Architecture Overview
--------------------------------------------------------

.. image:: /static/tachweb/architecture.png

Base Server Install                  [HA / S1 / S2 / S3 / L1 / L2]
=====================================================================

Note the [HA / S1 / S2 / S3 / L1 / L2] next to the topic, since it has all the machines in the list, the following procedures to the run on all machines mentioned inside the [] tags. 

To deploy Ubuntu 16.04, please view the following instruction manual: https://help.ubuntu.com/community/GraphicalInstall

After all Ubuntu OS been deployed and IP addresses has been configured, one could proceed with the following steps in this article.

Preparing the Machines              [HA / S1 / S2 / S3 / L1 / L2]
=====================================================================

The following steps has been deployed on all the instances mentioned in above tags [].

To speed up the base installation, Tachyonic created a tachlab project which could be downloaded from link_.

.. _link: https://github.com/vision1983/tachlab

.. code:: bash

 $ git pull https://github.com/vision1983/tachlab.git
 $ cd tachlab
 $ ./install.sh

MySQL Cluster   [S1 / S2 / S3]
===============================================================

Tachyonic decided to deploy the SQL cluster by making use of the Mariadb and Galera.

.. code:: bash

 $ sudo apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xF1656F24C74CD1D8
 $ sudo add-apt-repository 'deb [arch=amd64,i386,ppc64el] http://ftp.wa.co.za/pub/mariadb/repo/10.1/ubuntu xenial main'
 $ sudo apt-get update
 $ sudo apt-get -y install mariadb-server

Stop all mysql instances [S1 / S2 / S3]

.. code:: bash

 $ sudo systemctl stop mysql

Now we need to configure each server with its own SQL configuration file. 

Configure [S1]

.. code:: bash

 $ vi /etc/mysql/conf.d/galera.cnf

 [mysqld]
 binlog_format=ROW
 default-storage-engine=innodb
 innodb_autoinc_lock_mode=2
 bind-address=172.16.0.13
 wsrep_on=ON
 wsrep_provider=/usr/lib/galera/libgalera_smm.so
 wsrep_cluster_name="wingu_systems_cluster"
 wsrep_cluster_address="gcomm://172.16.0.13,172.16.0.12,172.16.0.14"
 wsrep_sst_method=rsync
 wsrep_node_address="172.16.0.13"
 wsrep_node_name="mariadb01"

Configure [S2]

.. code:: bash

 $ vi /etc/mysql/conf.d/galera.cnf

 [mysqld]
 binlog_format=ROW
 default-storage-engine=innodb
 innodb_autoinc_lock_mode=2
 bind-address=172.16.0.14
 wsrep_on=ON
 wsrep_provider=/usr/lib/galera/libgalera_smm.so
 wsrep_cluster_name="wingu_systems_cluster"
 wsrep_cluster_address="gcomm://172.16.0.13,172.16.0.12,172.16.0.14"
 wsrep_sst_method=rsync
 wsrep_node_address="172.16.0.14"
 wsrep_node_name="mariadb02"


Configure [S3]

.. code:: bash

 $ vi /etc/mysql/conf.d/galera.cnf
 
 [mysqld]
 binlog_format=ROW
 default-storage-engine=innodb
 innodb_autoinc_lock_mode=2
 bind-address=172.16.0.12
 wsrep_on=ON
 wsrep_provider=/usr/lib/galera/libgalera_smm.so
 wsrep_cluster_name="wingu_systems_cluster"
 wsrep_cluster_address="gcomm://172.16.0.13,172.16.0.12,172.16.0.14"
 wsrep_sst_method=rsync
 wsrep_node_address="172.16.0.12"
 wsrep_node_name="mariadb03"

Activating the SQL Cluster [S1, then S2, then S3]
-------------------------------------------------------

The command to start a Galera cluster galera_new_cluster. 

Note the then, in-between, this indicates that the steps below, to be run sequentially starting with the first host, and once completed, continue to the second and so third. 

.. code:: bash

 $ sudo galera_new_cluster
 $ sudo systemctl start mysql
 $ mysql -u root -p -e "SHOW STATUS LIKE 'wsrep_cluster_size'"
 +--------------------+-------+
 | Variable_name      | Value |
 +--------------------+-------+
 | wsrep_cluster_size | 1     |     # Note Value == 2 ( Only if second SQL server successfully connected to host)
 +--------------------+-------+     # Value == 3 (Once the third SQL server connected to the cluster)

Verify if the server connected successfully by creating a database and verifying if exists amongst all the SQL servers. 

Web Server [L1 / L2]
=======================================

Since the Luxon Framework conforms to the Web Server Gateway Interface (WSGI) standards, we going to front-end it with Apache and mod_wsgi. 

Installing Apache on the webserver, configuring Apache to explicit listen only from the internal address.

.. code:: bash

 $ apt-get install apache2
 $ vi /etc/apache2/ports.conf

 Listen 172.16.0.18:80

Restart the service, for the changes to take effect. Further configurations to be updated.

.. code:: bash

 $ service apache2 restart

HAProxy [HA]
=============================

We going to use HAProxy to round-robin the HTTP requests, distributing the load on the web servers.

Furthermore, extending the tcp load balancing all SQL queries to all SQL servers. (since mariadb / galera configuration enables writing to be performed on any of the SQL servers at any given time.)

Installing HAProxy 

.. code:: bash

 $ apt-get install haproxy

Configure the HAProxy, please note that the following would need to be prepended to the existing configuration. 
 
.. code:: bash

 $ vi /etc/haproxy/haproxy.cfg

 backend web-backend
    balance roundrobin
    server lab1 172.16.0.18:80 check
    server lab2 172.16.0.19:80 check

 frontend http
    bind *:80
       mode http
       acl url_blog path_beg /blog
       use_backend web-backend

 listen galera
    bind 172.16.0.16:3306
       balance source
       mode tcp
       option tcpka
       server node1 172.16.0.12:3306 check weight 1
       server node2 172.16.0.13:3306 check weight 1
       server node2 172.16.0.14:3306 check weight 1

Restart the server and verify that the ports are listening correctly

.. code:: bash

 $ service  haproxy restart
 $ netstat -tunlp | egrep '3306|80'
 tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      -
 tcp        0      0 172.16.0.16:3306        0.0.0.0:*               LISTEN      -

Luxon Framework   [L1 / L2] 
=====================================

Finally, now that we have full redundancy amongst different servers, we could continue to deploy the Luxon Framework. In this document we are going to cover the infinitystore and netrino.


Infinity Stone [L1 / L2]
-------------------------------------

Keep an eye out for changes, this to be populated.

Github project to be found at infinitystone_.

.. _infinitystone: https://github.com/TachyonicProject/infinitystone

Netrino [L1 / L2]
-------------------------------------

Keep an eye out for changes, this to be populated.

Github project to be found at netrino_.

.. _netrino: https://github.com/TachyonicProject/netrino







