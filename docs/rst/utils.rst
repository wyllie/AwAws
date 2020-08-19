=========
Utilities
=========

.. automodule:: AwAws.Utils

Env
===

This module tries to be smart about grabbing environment variables.
It catches and ignores Exceptions for cases were an environment variable
has not been set - just returns None.  It also allows you to unset an
environment variable, also fails silently if you try to unset an environemnt
variable that has not been set.


.. autoclass:: AwAws.Utils.env.Env
   :members:
   :inherited-members:

