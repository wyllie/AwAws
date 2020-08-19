=======
Session
=======

These are the main modules that connect to AWS.  Since AwAws was orginally
intended to be used from Lamda functions, these modules implement caching
techniques to take adavanatge of Lambda function warm starts.

Generally speaking, the modules here are only used by other modules in the AwAws
package.  That said, this module can be used directly to connect to AWS using
either boto3 or botocore.  The advantage is that you still get to take
advantage of the caching which can give a significant speed improvement when
using lambda functions.

.. automodule:: AwAws.Session


Session
=======

Manage AWS client sessions - usually built directly through botocore.

.. autoclass:: AwAws.Session.session.Session
   :members:
   :inherited-members:


Resource
========

Manage AWS resource session - these are usually implemented through boto3.

.. autoclass:: AwAws.Session.resource.Resource
   :members:
   :inherited-members:
