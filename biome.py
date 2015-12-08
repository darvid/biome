"""
    biome
    ~~~~~

    Provides painless access to namespaced environment variables.
"""
import ast
import os
import pathlib
import sys

import attrdict


__all__ = ("EnvironmentError", "Habitat")


# Create a reference to the module so it doesn't get deleted
# See http://stackoverflow.com/a/5365733/211772
_module_ref = sys.modules[__name__]


def _sanitize_prefix(prefix):
    return prefix.upper().rstrip("_")


class EnvironmentError(KeyError):
    """Raised when something went wrong accessing the environment.

    This exception subclasses ``KeyError`` for compatibility with
    ``os.environ`` in tests.

    """

    @classmethod
    def not_found(cls, prefix, name):
        return cls("'%s_%s' does not exist in the environment" %
                   (prefix, name.upper()))


class Habitat(attrdict.AttrDict):
    """Provides attribute/map style access to a set of namespaced
    environment variables.

    Environment variable values are implicitly converted to Python
    literals when possible, and can also be explicitly accessed through
    the ``get``, ``get_bool``, ``get_int``, and ``get_path`` methods.

    Args:
        prefix (str): The prefix to use, sans trailing underscore.

    """

    def __init__(self, prefix):
        self._setattr("_prefix", _sanitize_prefix(prefix))
        super(Habitat, self).__init__(self.get_environ(self._prefix))

    @classmethod
    def get_environ(cls, prefix):
        """Retrieves a list of environment variables and their values
        for a given namespace.

        Args:
            prefix (str): The prefix, without a trailing underscore.

        Returns:
            list: A list of environment variable keys and values.

        """
        return ((key[len(prefix) + 1:], value)
                for key, value in os.environ.items()
                if key.startswith("%s_" % prefix))

    def get_prefixed_name(self, name):
        """Builds an environment variable name.

        Args:
            name (str): The case-insensitive, unprefixed variable name.

        Returns:
            str: The full environment variable name, including prefix.

        """
        return "%s_%s" % (self._prefix, name.upper())

    def get(self, name, default=None):
        """A more explicit alternative to attribute or item access.

        Args:
            name (str): The case-insensitive, unprefixed variable name.
            default: If provided, a default value will be returned
                instead of throwing ``EnvironmentError``.

        Returns:
            The value of the environment variable. The value is
            implicitly converted to a Python literal (such as ``int``
            or ``bool``) when possible.

        Raises:
            EnvironmentError: If the environment variable does not
                exist, and ``default`` was not provided.

        """
        try:
            return self[name]
        except EnvironmentError:
            if default is not None:
                return default
            raise

    def get_bool(self, name, default=None):
        """Retrieves an environment variable value as ``bool``.

        Integer values are converted as expected: zero evaluates to
        ``False``, and non-zero to ``True``. String values of ``'true'``
        and ``'false'`` are evaluated case insensitive.

        Args:
            name (str): The case-insensitive, unprefixed variable name.
            default: If provided, a default value will be returned
                instead of throwing ``EnvironmentError``.

        Returns:
            bool: The environment variable's value as a ``bool``.

        Raises:
            EnvironmentError: If the environment variable does not
                exist, and ``default`` was not provided.
            ValueError: If the environment variable value could not be
                interpreted as a ``bool``.

        """
        if name not in self:
            if default is not None:
                return default
            raise EnvironmentError.not_found(self._prefix, name)
        try:
            return bool(self.get_int(name))
        except ValueError:
            value = self[name].lower()
            if value not in ("true", "false"):
                raise ValueError("cannot interpret %r as boolean" % self[name])
            return value == "true"

    def get_int(self, name, default=None):
        """Retrieves an environment variable as an integer.

        Args:
            name (str): The case-insensitive, unprefixed variable name.
            default: If provided, a default value will be returned
                instead of throwing ``EnvironmentError``.

        Returns:
            int: The environment variable's value as an integer.

        Raises:
            EnvironmentError: If the environment variable does not
                exist, and ``default`` was not provided.
            ValueError: If the environment variable value is not an
                integer with base 10.

        """
        if name not in self:
            if default is not None:
                return default
            raise EnvironmentError.not_found(self._prefix, name)
        return int(self[name])

    def get_path(self, name, default=None):
        """Retrieves an environment variable as a ``pathlib.Path``
        object.

        Requires the `pathlib`_ library if using Python <= 3.4.

        Args:
            name (str): The case-insensitive, unprefixed variable name.
            default: If provided, a default value will be returned
                instead of throwing ``EnvironmentError``.

        Returns:
            pathlib.Path: The environment variable as a ``pathlib.Path``
                object.

        Raises:
            EnvironmentError: If the environment variable does not
                exist, and ``default`` was not provided.

        .. _pathlib:
           https://pypi.python.org/pypi/pathlib/

        """
        if name not in self:
            if default is not None:
                return default
            raise EnvironmentError.not_found(self._prefix, name)
        return pathlib.Path(self[name])

    def refresh(self):
        """Update all environment variables from ``os.environ``.

        Use if ``os.environ`` was modified dynamically *after* you
        accessed an environment namespace with ``biome``.

        """
        super(Habitat, self).update(self.get_environ(self._prefix))

    def __contains__(self, name):
        return super(Habitat, self).__contains__(name.upper())

    def __getitem__(self, name):
        name = name.upper()
        if name.startswith("_"):
            return super(Habitat, self).__getitem__(name)
        try:
            value = super(Habitat, self).__getitem__(name)
        except KeyError:
            raise EnvironmentError.not_found(self._prefix, name)
        try:
            # Attempt to parse value as a Python literal
            if value.lower() in ("true", "false"):
                value = value.title()
            value = ast.literal_eval(value)
        except (SyntaxError, ValueError):
            name_upper = name.upper()
            # Return a ``pathlib.Path`` object iff:
            # * value contains the default OS path separator
            # * the substring 'PATH', 'DIR', or 'FILE' in the var name
            if (os.path.sep in value and
                    "PATH" in name_upper or
                    "DIR" in name_upper or
                    "FILE" in name_upper):
                value = pathlib.Path(value)
        return value

    def __repr__(self):
        return u"<%s(%r, %r)>" % (
            self.__class__.__name__,
            self._prefix,
            dict.__repr__(self)
        )


class _Biome(attrdict.AttrDict):
    def __getattr__(self, name):
        if name == "_lib":
            return _module_ref
        try:
            return self[name.upper()]
        except KeyError:
            if name.startswith("_"):
                raise
            name = _sanitize_prefix(name)
            if name not in self and not name.startswith("_"):
                self[name] = _module_ref.Habitat(name)
            return self[name]

    def __repr__(self):
        return u"<%s(%s)>" % (self.__class__.__name__, dict.__repr__(self))


sys.modules[__name__] = _Biome()
for prop in ("file", "name"):
    object.__setattr__(sys.modules[__name__], "__%s__" % prop,
                       locals()["__%s__" % prop])
sys.modules["%s._lib" % __name__] = _module_ref
