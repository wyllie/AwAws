========
Security
========

.. automodule:: AwAws.Security.kms

KMS
=================

This library is used to implement *envelope* encryption on data objects.
The idea is that there is a master key store in the AWS KMS system which
is used to encrypt unique encryption keys which have been used to encrypt
data objects.

Usage looks something like this::

    from AwAws.Security.kms import KMS
    
    test_obj = {
        'this': 'is a test',
        'with': ['a', 'list', 'of', 'items'],
        'and': {
            'some': 'nested info'
        }
    }
    
    kms = KMS()
    kms.set_encryption_regions('us-east-2')
    kms.set_master_keys('arn:aws:kms:us-east-2:acct_num:key/key_id')
    cipher_obj = kms.encrypt_object(test_obj)
    decrypted_obj = kms.decrypt_object(cipher_obj)
    
    # Check it
    print('ENCRYPTED', cipher_obj)
    print('DECRYPTED', decrypted_obj)
    assert test_obj == decrypted_obj
    print('Yeah! Got it!')


.. autoclass:: AwAws.Security.kms.KMS
   :members:
   :inherited-members:


