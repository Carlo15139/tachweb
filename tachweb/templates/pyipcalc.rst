PyIPCalc
========

pyipcalc is module developed for doing simple ip calculations needed by some python applications. Python 3 has built-in 'ipaddress' module providing many of the desired functionality. However I needed a common interface and support within both Python 2.7 and 3.x. At the time there were many modules some which were complex and others that were broken at the time. pyipcalc is simple and contributions are welcome!

Project Status: Production / Active

Quick Links
-----------

* `Website <http://www.tachyonic.co.za/pyipcalc>`__.
* `GITHUB Code <https://github.com/TachyonicProject/pyipcalc>`__.
* `Issues <https://github.com/TachyonicProject/pyipcalc/issues>`__.

Installation
------------

PyIPCalc currently fully supports `CPython <https://www.python.org/downloads/>`__ 2.7 and 3.x

A package is availible on PyPI.
Installing it is as simple as:

.. code:: bash

    $ pip install pyipcalc

Source Code
-----------

Code is hosted on `GitHub <https://github.com/TachyonicProject/pyipcalc>`_. Making the code easy to browse, download, fork, etc. Pull requests are always welcome!

Clone the project like this:

.. code:: bash

    $ git clone https://github.com/TachyonicProject/pyipcalc.git

Once you have cloned the repo or downloaded a tarball from GitHub, you
can install pyipcalc like this:

.. code:: bash

    $ cd pyipcalc
    $ pip install .

Or, if you want to edit the code, first fork the main repo, clone the fork
to your desktop, and then run the following to install it using symbolic
linking, so that when you change your code, the changes will be automagically
available to your app without having to reinstall the package:

.. code:: bash

    $ cd pyipcalc
    $ pip install -e .

You can manually test changes to pyipcalc by switching to the
directory of the cloned repo:

.. code:: bash

    $ cd pyipcalc/tests
    $ python test.py

Using PyIPCalc
--------------

.. code:: bash

	$ pyipcalc 192.168.0.0/24
	PyIPCalc 2.0.0

		Network Prefix: 192.168.0.0/24
		Network Address: 192.168.0.0
		First IP Address: 192.168.0.1
		Last IP Address: 192.168.0.254
		Broadcast Address: 192.168.0.255
		Netmask: 255.255.255.0

IPV6
----
IPV6 is supported, you can simply just provide an IPV6 prefix.

Development Module
------------------
.. code:: python

	$ python
	>>> import pyipcalc
	>>> net = pyipcalc.IPNetwork('192.168.0.0/24')
	>>> print net.prefix()
	>>> 192.168.0.0/24
	>>> print net.network()
	>>> 192.168.0.0
	>>> print net.first()
	>>> 192.168.0.1
	>>> print net.last()
	>>> 192.168.0.254
	>>> print net.broadcast()
	>>> 192.168.0.255
	>>> print net.mask()
	>>> 255.255.255.0

	>>> for ip in net:
	...     print ip
	... 
	192.168.0.0/32
	192.168.0.2/32
	........
	........
	192.168.0.254/32
	192.168.0.255/32
	>>>  

	>>> test = pyipcalc.IPIter('10.10.10.0/24',26)
	>>> for net in test:
	...     print net
	... 
	10.10.10.0/26
	10.10.10.64/26
	10.10.10.128/26
	10.10.10.192/26
	>>> 

	>>> test = pyipcalc.IPIter('10.10.10.0/24',26)
	>>> for net in test:
	...     print net.first()
	...     print net.last()
	... 
	10.10.10.1
	10.10.10.62
	10.10.10.65
	10.10.10.126
	10.10.10.129
	10.10.10.190
	10.10.10.193
	10.10.10.254
	>>> 

Converting IPv4 to 32bit Decimal to store in database.

.. code:: python

	>>> print pyipcalc.ip2dec('192.168.0.0',4)
	>>> 3232235520
	>>> print pyipcalc.dec2ip(3232235520,4)
	>>> 192.168.0.0
	>>> 

Converting IPv6 to 128bit Decimal to store in database.

.. code:: python

	>>> print pyipcalc.ip_to_int('ffff:0000:0000:0000:0000:0000:0000:0000')
	>>> 340277174624079928635746076935438991360
	>>> print pyipcalc.int_to_ip(340277174624079928635746076935438991360,6)
	>>> ffff:0000:0000:0000:0000:0000:0000:0000

Typically you will need two 64bit columns in a database to store 128bit IPv6 address.

.. code:: python

	>>> print pyipcalc.int_128_to_64(340277174624079928635746076935438991360)
	>>> [18446462598732840960L, 0L]
	>>> print pyipcalc.int_64_to_128(18446462598732840960L,0L)
	>>> 340277174624079928635746076935438991360

Checking wether one subnet contains another:

.. code:: python

	>>> net = pyipcalc.IPNetwork('192.168.0.0/24')
	>>> net1 = pyipcalc.IPNetwork('192.168.0.1/32')
	>>> net2 = pyipcalc.IPNetwork('192.168.1.0/24')
	>>> net.contains(net1)
	>>> True
	>>> net.contains(net2)
	>>> False

	>>> if net1 in net: print (True)
	>>> 
	... True
	>>> if net not in net2: print (False)
	>>> 
	... False

Note that if net == net1, contains() will return True

Finding the smallest common supernet that contains two subnets:

.. code:: python

	>>> pyipcalc.supernet(net1,net2)
	>>> 192.168.0.0/23

	>>> net1 = pyipcalc.IPNetwork('192.168.0.0/24')
	>>> net2 = pyipcalc.IPNetwork('192.168.1.0/24')
	>>> net3 = pyipcalc.IPNetwork('192.168.2.0/24')
	>>> net1 + net2 + net3
	>>> 192.168.0.0/22

The supernet() function also takes a third optional argument, which specifies the minimum prefix length to be searched. Consider for example the case where one searches for the common supernet of 128.0.0.1/32 and 10.0.0.1/32. Because the former has a 1 in the left most bit, while the latter has a 0, the only common supernet would be 0.0.0.0/0, which might not be the desirable outcome. For that reason, one could limit the search. If a common supernet is found within the search limits, it is returned, otherwise 'None' is returned. If this limit is not specified, the default for IPv4 is 8, and for IPv6 is 16.

.. code:: python

	>>> net3 = pyipcalc.IPNetwork('10.0.0.1/32')
	>>> pyipcalc.supernet(net1,net3)
	>>> pyipcalc.supernet(net1,net3,0)
	>>> 0.0.0.0/0
	>>> net4 = pyipcalc.IPNetwork('127.0.0.1/32')
	>>> pyipcalc.supernet(net3,net4)
	>>> pyipcalc.supernet(net3,net4,1)
	>>> 0.0.0.0/1
	>>> net5 = pyipcalc.IPNetwork('172.16.0.0/8')
	>>> pyipcalc.supernet(net2,net5)
	>>> pyipcalc.supernet(net2,net5,0)
	>>> 128.0.0.0/1
