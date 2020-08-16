=============
Configuration
=============

.. automodule:: AwAws.Config.env

Env
===

This module will get environment variables from the operating system.

Usage looks something like this::

    from AwAws.Config.env import Env
    
    env = Env()
    blargh = env.get_env('BLARGH')

    print('BLARGH is currently set to:', blargh)


.. autoclass:: AwAws.Config.env.Env
   :members:
   :inherited-members:


