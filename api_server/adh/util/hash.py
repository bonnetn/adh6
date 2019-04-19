import hashlib


def ntlm_hash(txt):
    """
    NTLM hashing function
    wow much security such hashing function
    Needed by MSCHAPv2.
    """

    return hashlib.new('md4', txt.encode('utf-16le')).hexdigest()
