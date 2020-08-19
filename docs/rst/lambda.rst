======
Lambda
======

.. automodule:: AwAws.Lambda.base
.. automodule:: AwAws.Lambda.tools

Lambda
======

.. autoclass:: AwAws.Lambda.base.Lambda
   :members:
   :inherited-members:

Lambda Tools
============

Currently the only tool is called WhipIt.  It is meant to be installed
in a lambda that is run by CloudWatch Events and run every 30 minutes
or so.  When it runs, it invokes the lambdas in its target list but
short circuits the logic of the lambda.  This keeps the lambda warm
and helps to avoid, but does not eliminate, cold starts.

.. autoclass:: AwAws.Lambda.tools.LambdaTools
   :members:
   :inherited-members:
