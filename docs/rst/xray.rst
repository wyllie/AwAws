====
XRay
====

.. automodule:: AwAws.XRay.xray

XRay
=================

This library is used to add XRay tracing and analytics to monitor our
platform.  XRay is an AWS services that provides good insights into
how our distibuted system is running.

This system has a few pieces.  First you have to **turn_it_on** by
either calling the constructor with turn_it_on=True or setting
an environment variable (not implemented yet).

- **segments**, and optional **subsegments** are used to identify different
  parts of the code in a heirarcial way.  Keep in mind that these need to
  be *closed*. 
- **Annotations** are used to orgainze/search for traces using the
  XRay console.
- **Metadata** can be added to provide information about data being
  used in the trace.

The way XRay is integrated with AWS Lambda is that the Lambda system
uses the *segment* so only *subsegments* are available.  Trying to
use *begin_segment* will throw some very odd errors when being used
in a lambda (you have been warned).

The imports on this module are called from within the constructor.
The reason for this is that the xray-sdk needs to be loaded last
so that it can patch the other SDKs.  This also allows us to easily
turn the globally turn XRay feature on and off as well as moving all
of the logic for on/off out of the caller functions.

Usage in a lambda looks something like this::

    from AwAws.Xray.xray import Xray
    
    test_obj = {
        'this': 'is a test',
        'with': ['a', 'list', 'of', 'items'],
        'and': {
            'some': 'nested info'
        }
    }
    
    xray = XRay(turn_it_on=True)  # the default is off
    kms = KMS()
    xray.begin_subsegment('kms')  # creates a subsegment called kms
    kms.set_encryption_regions('us-east-2')
    kms.set_master_keys('arn:aws:kms:us-east-2:acct_num:key/key_id')
    cipher_obj = kms.encrypt_object(test_obj)

    xray.put_annotation('object_type', 'object_type_description')  # key/value
    xray.put_metadata('cipher_obj', test_obj)  # add some info about the object
    decrypted_obj = kms.decrypt_object(cipher_obj)
    
    # Check it
    print('ENCRYPTED', cipher_obj)
    print('DECRYPTED', decrypted_obj)
    assert test_obj == decrypted_obj
    print('Yeah! Got it!')

    xray.end_subsegment()


.. autoclass:: AwAws.XRay.xray.XRay
   :members:
   :inherited-members:


