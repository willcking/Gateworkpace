from solana.publickey import PublicKey


class EoaAccountSOL:
    def __init__(self, address, prikey):
        self.address = PublicKey(address)
        self.private_key = prikey
