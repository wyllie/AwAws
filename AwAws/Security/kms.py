import aws_encryption_sdk as aes
import json

from AwAws.Session.session import Session


class KMS:
    '''
    :param region_name: the region we are using

    .. note::  There are two type of regions being used here: \n
        #. the region we are connecting to to run the code
        #. the regions(s) where we want to run the encryption since
           KMS encryption keys are region specific and cannot be copied
           across regions
    .. note:: in order to use multiple regions, multiple master_keys
           also need to be defined
    '''

    def __init__(self, region_name=None):

        self.enc_regions = []
        self.master_keys = []
        self.key_provider = None
        self.kms = Session(region_name).get_client('kms')


    def set_encryption_regions(self, regions=[]):
        'master encryption keys are locked to a specific region'
        if type(regions) == str:
            self.enc_regions.append(regions)
        else:
            self.enc_regions.extend(regions)


    def set_master_keys(self, master_keys=[]):
        'list of master keys to use'
        if type(master_keys) == str:
            self.master_keys.append(master_keys)
        else:
            self.master_keys.extend(master_keys)


    def set_key_provider(self):
        'called by en(de)crypt_it(), get the master key provider'
        try:
            assert len(self.enc_regions) > 0
            assert len(self.master_keys) > 0

            self.key_provider = aes.KMSMasterKeyProvider(
                botocore_session=self.kms,
                key_ids=self.master_keys,
                region_names=self.enc_regions
            )
        except AssertionError:
            raise Exception('Region or Master Keys not set')
        except Exception as e:
            raise Exception('Could not set key_provider', e)


    def encrypt_object(self, obj_to_encrypt):
        'encrypt a python object'
        try:
            # need to convert the object to a string
            json_to_encrypt = json.dumps(obj_to_encrypt)
        except Exception as e:
            raise Exception('Could not serialize object', e)

        return self.encrypt_it(json_to_encrypt)


    def decrypt_object(self, cipher_object):
        'returns python object from a given cipher object'
        decrypted_text = self.decrypt_it(cipher_object)
        return json.loads(bytes.decode(decrypted_text))


    def encrypt_it(self, text_to_encrypt):
        'encrypt a block of text'
        cipher_obj = {}

        self.set_key_provider()
        (cipher_obj['cipher_text'], cipher_obj['encryptor_header']) = aes.encrypt(
            source=text_to_encrypt,
            key_provider=self.key_provider
        )
        return cipher_obj


    def decrypt_it(self, cipher_obj):
        'decrypt encrypted text'
        self.set_key_provider()
        (decrypted_text, decryptor_header) = aes.decrypt(
            source=cipher_obj['cipher_text'],
            key_provider=self.key_provider
        )
        try:
            assert cipher_obj['encryptor_header'] == decryptor_header
        except AssertionError:
            raise Exception('Encryption headers do not match!!!')

        return decrypted_text

