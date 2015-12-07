Usage
=====

Accessing namespaces
--------------------

Environment *namespaces*, or sets of environment variables that share
a common prefix, are grouped into :class:`~._lib.Habitat` objects.
For example, the following environment variables are part of the
``YOURAPP`` namespace::

    YOURAPP_HOST="server.com"
    YOURAPP_PORT=8000
    YOURAPP_DEBUG="true"

**biome** dynamically populates namespaces on attribute access to the
``biome`` *"module"*, which is actually a class injected into
:data:`sys.modules`. This results in a slightly magical, but extremely
convenient drop-in configuration provider for your application.

.. code-block:: pycon

    >>> import biome
    >>> biome.YOURAPP.host
    "server.com"

.. note::
   **biome** expects that your environment variable prefixes always
   carry a trailing underscore, separating them from the suffix, or
   variable name. For instance, the variable ``YOURAPPDEBUG`` must be
   changed to ``YOURAPP_DEBUG`` if you want it included in the
   ``YOURAPP`` namespace.


Accessing variables
-------------------

Namespaced environment variables can be accessed in the way you'd
expect (via attributes), and are automatically converted to ``int``,
``bool``, and :class:`pathlib.Path` objects whenever possible.

.. code-block:: python

    # YOURAPP_SECRET_KEY='~/.secret_key'
    secret_key = biome.YOURAPP.secret_key.read_text()

You can also use any of the getters in the :class:`~._lib.Habitat` class
to explicitly coerce types, or if you want to provide default values.

.. code-block:: python

    debug = biome.YOURAPP.get_bool("debug", False)
