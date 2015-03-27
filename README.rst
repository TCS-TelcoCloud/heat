============
HEAT Changes
============

* HEAT module is updated to enable orchestration of VNF with vnfsvc

Setup for REDHAT
----------------

* Heat updates::

    $ git clone https://github.com/TCS-TelcoCloud/OpenVNFManager.git 

    $ Copy heat/heat/common/config.py to /usr/lib/python2.7/site-packages/heat/common/config.py

    $ Copy heat/heat/engine/clients/__init__.py to /usr/lib/python2.7/site-packages/heat/engine/clients/__init__.py

    $ Copy heat/heat/engine/clients/os/vnfsvc.py to /usr/lib/python2.7/site-packages/heat/engine/clients/os/vnfsvc.py

    $ Copy heat/heat/engine/resource.py to /usr/lib/python2.7/site-packages/heat/engine/resource.py
    
    $ Copy heat/heat/engine/resources/vnfsvc/__init__.py to /usr/lib/python2.7/site-packages/heat/engine/resources/vnfsvc/__init__.py 

    $ Copy heat/heat/engine/resources/vnfsvc/vnfsvc.py to /usr/lib/python2.7/site-packages/heat/engine/resources/vnfsvc/vnfsvc.py

    $ Copy heat/heat/engine/resources/vnfsvc/vnf_template.py to /usr/lib/python2.7/site-packages/heat/engine/resources/vnfsvc/vnf_template.py

    $ Update entry_points.txt with "vnfsvc = heat.engine.clients.os.vnfsvc:VnfsvcClientPlugin" under [heat.clients]

    $ Update /etc/heat/heat.conf with the line [clients_vnfsvc]

* After installing vnfsvc, python-vnfsvcclient and HEAT updates, run the setup as detailed in vnfsvc_examples
