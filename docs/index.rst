.. AwAws documentation master file

==============================
AwAws a boto3/botocore Wrapper
==============================

AwAws is a Python wrapper around the boto3/botocore libraries provided by AWS.
It was written to be installed as a layer on AWS Lambda and is primarily intended
to be used with serverless applications (Lambda functions) on AWS.  That said, the
library can also be used with any Python program that needs access to AWS APIs
including local command line tools or daemons running on EC2/ECS/Fargate, etc.


AwAws SDK Reference
===================

.. toctree::
   :maxdepth: 1

   rst/api
   rst/db
   rst/events
   rst/lambda
   rst/orgs
   rst/security
   rst/session
   rst/shared
   rst/sqs
   rst/storage
   rst/utils
   rst/xray

Exceptions
==========

   <TODO>



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
