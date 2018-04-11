About
=====

    The Tachyonic Project is an eco system of Open Source Packages that, when used together, becomes an orchestrator of orchestrators. It allows for rapid development to become the single pane of glass into all your systems. As the glue between your OSS, BSS and Networked elements, it meets the need of all your orchestration and automation requirements. Purposely built for large operators such as mobile telephone operators, commercial and home broadbrand providers, tier 1 network operators, large data centre and cloud providers by expierenced network engineers for network engineers.

    Tachyonic lets you automate the creation, monitoring, and deployment of resources in your environment. The unique environment platform is designed to be vertically and horizontally scalable. The platform does not neccessarily automate all the processes but also works collectively with other orchestrators and automation systems. 

    Christiaan Rademan (@cfrademan) is the original creator of the Tachyonic Project, and currently develops the project along with author Dave Kruger (@vuader) and several other contributors. Tachyonic is developed by a growing community of users and contributors just like you.

Scalable
~~~~~~~~~

    Its build on on the principle of isolated projects which are responsible for specific functionality and features all using the same framework (Luxon) to provide rapid development and north- and south-bound interfaces. 

    One important feature is that all interfaces into Tachyonic can be publically exposed and redundantly deployed over several regions, domains and endpoints. All application interfaces are based on the well known *JSON using RESTAPI* method. 

Code
~~~~
    The project is primarily developed on Python and supports both version 3.5 and 3.6. (3.6 recommended) 

    Design emphasizes on the MVC pattern (Model, View, Controller) and build on best practice cloud infrastructure design principles. 

Endpoints
~~~~~~~~~

    Endpoints provide additional functionality to the system. You may add your own, or use some of the endpoints bundled in the Tachyonic Project. Some examples of these are:

    * Netrino - used for orchestration via service templating,
    * InfinityStone - used for AAA (Authentication, Authorization and Accounting),
    * Yoshii - used for Telemetry. 
    * Photonic - a Web UI.
    * Telepathic - responsible for load distribution between tasks.

    All endpoints providing services are fully scalable by just adding more hardware and using HA proxies such as F5 or opensource projects.
    Minion workers and deamons perform tasks such as deploying configurations built using YANG templates and collecting Telemetry data and SNMP counter values.

Storage
~~~~~~~
    A controversial subject was finding a way to store large amounts of data in a secure, redundant manner such as those collected and consumed by the Telemetry service. Hence the Katalog and Kiloquad project was initiated. Its a simple object store being stricly built for our purposes with tight integration to other projects as such Python's Pandas. 

    Databases used are SQLite, Mysql or Mariadb.

Opensource
~~~~~~~~~~
    All projects part of Tachyonic is open-source and freely availible. Commercial support can be provided by relevant skilled contractors or organizations in the future. The source code for all projects can be found on: https://github.com/orgs/TachyonicProject

    The project is licesend under the BSD-3 Clause license. `More here... <http://www.tachyonic.org/rst/opensource>`_

Project Status
==============

    Early development phase. A project schedule and planning detailed status: `Project Scope <http://www.tachyonic.org/rst/project_schedule>`_
