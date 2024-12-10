from Crypto.PublicKey import RSA  # provided by pycryptodome


def generate_private_key(input):
    key = RSA.generate(2048)
    private = key.export_key()
    public = key.publickey().export_key()
    
    return private, public