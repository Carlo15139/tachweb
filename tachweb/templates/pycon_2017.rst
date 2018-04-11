Intro: (10 mins)

Meet Bob. Bob is a Network Administrator at a Service Provider.
As a well seasoned network engineer, he's been building packet pushing networks since the days when IP shared bandwidth with IPX, Appletalk, DECnet etc. He is a well rounded network engineer with robust set of networking skills. He mastered making, shaping of networks with his tool set such as Spanning Tree, RAPS, Vlans, VXLAN and MPLS.


However, Bob's world is changing. Networks are not what they used be. Today's networks are growing more rapidly than ever. This means there are more devices to manage and also more data produced by these devices to work with. Doing things manually just don't scale anmore. Bob has no other option to turn to automation.


In the Devops world these issues have been and are being addressed. The Networking universe is lagging behind. Standard Bodies and Vendors have started coming up with solutions such as Openflow and NETCONF, but there are limits.


Also, many Open source projects (most of them written in Python) and proprietary solutions have joined the scene, which we will talk about.


So Bob has options, but… none of them has all the answers. Except for one!


Introduction to Tachyonic Open Source Project (10 mins)

Why Python?
** (you probably know some of the answer already)

What is Tachyonic?
** Tachyonic framework is intended to control a large pool of services such as cloud, networking, dns, email managed through a single dashboard. The goal here is to have a "single pane of glass” view. Tachyonic scale is only dependent on the deployment method used and is designed to be massively horizontally scalable. It's all open-source and completely customizable.

Modular - extensible
All interfaces such as API endpoints and Dashboard views are fully extensible via plugins/modules. All you need to do is write the bit of python to meet your need, and plug it into the Tachyonic framework.
Components and endpoints can run on the same Server, or different ones.

API and UI
** Tachyonic comes with both a RESTful API, as well as a UI for those who wish to use it. In fact the UI simply uses the API in the back-end

Multi-Tenancy
** With Tachyonic you get a framework that us Multi-Tenant, and Multi-Tiered. That means you can use it to add customers, and Customers can even be resellers that have their own customers. Tachyonic takes care of who is allowed access to what.

What you get (10 mins)

We have done all the hard work for you:
User login and RBAC
Separate Domains
UI
API
* WSGI Framework


  What you need to code

  You may simply write the python you require, and plug it in! Single extendable portal, restapi framework does it all!


  Use cases

  Build customer portals to provision services in addition to integrated helpdesk and payment gateways.

  Build Billing and Telemetry services on top of Python using well-known open-source projects such as Pandas for time series data.

  Automate deployment and monitoring of network devices

  With knowledge of Python and Tachyonic, you may never have to look at a new system ever again!

