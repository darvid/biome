.. biome documentation master file, created by
   sphinx-quickstart on Sat Dec  5 18:45:36 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to biome
================

**biome** is a tiny library that enables developers to configure their
applications from the environment cleanly, quickly, and unobtrusively.

Storing application configuration in environment variables is in many
cases considered a `best practice`_, but loading configuration values
from the environment is not particularly :abbr:`DRY (Don't Repeat Yourself)`.

.. code-block:: python

    import os
    server_host = os.environ["MYAPP_HOST"]
    server_port = int(os.environ["MYAPP_PORT"])
    debug = os.environ["MYAPP_DEBUG"].lower() in ("true", "1")

With **biome**, you can effectively namespace your application
configuration with environment variable prefixes, and access config
values through either attributes or items, whichever you prefer.

.. code-block:: python

    import biome
    config = biome.myapp  # or biome.MYAPP, or biome.MyApp
    debug = config.debug  # or config.DEBUG -- this returns a boolean
    bind = "%s:%d" % (config.host, config.port)


.. _best practice:
   http://12factor.net/config


Documentation Contents
----------------------
.. toctree::
   :maxdepth: 2

   features
   api
