===============
SharedResources
===============

.. automodule:: AwAws.SharedResources

Parameters
==========

Connects to the SSM Parameter Store service on AWS.  This can
be really handy for storing configuration parameters as well as
things like passwords which can be stored securely.  Another
nice benefit is that the parameter store service tracks the
history of the parameters so you can see if/how they have changed
over time.

.. autoclass:: AwAws.SharedResources.parameters.Parameters
   :members:
   :inherited-members:

