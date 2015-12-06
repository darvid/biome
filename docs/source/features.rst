Features
========

- **Zero-setup, global access to environment variable namespaces.**
  No instantiation needed.

  .. code-block:: python

      # lib/database.py
      import biome
      print(biome.database.driver)

      # lib/logging.py
      import biome
      print(biome.logging.rsyslog)

- **Implicit type coercion.** Or explicit, whatever floats your
  boat.

  .. code-block:: pycon

      >>> biome.myapp.host
      "0.0.0.0"
      >>> biome.myapp.port
      8000
      >>> biome.myapp.debug
      True
      >>> biome.myapp.static_path
      PosixPath("/var/www/static")
      >>> biome.myapp.get_int("port")
      8000
