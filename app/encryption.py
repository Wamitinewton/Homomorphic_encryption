from phe import paillier
import json
from typing import List, Tuple

class HomomorphicEncryption:
    """
    Wrapper class for Paillier Homomorphic Encryption.
    Paillier allows addition and scalar multiplication on encrypted data.
    """
    
    @staticmethod
    def generate_keypair() -> Tuple[paillier.PaillierPublicKey, paillier.PaillierPrivateKey]:
        """Generate a new public/private keypair"""
        public_key, private_key = paillier.generate_paillier_keypair(n_length=512)
        return public_key, private_key
    
    @staticmethod
    def serialize_public_key(public_key: paillier.PaillierPublicKey) -> str:
        """Convert public key to JSON string for transmission"""
        return json.dumps({'n': public_key.n})
    
    @staticmethod
    def deserialize_public_key(key_str: str) -> paillier.PaillierPublicKey:
        """Recreate public key from JSON string"""
        key_data = json.loads(key_str)
        return paillier.PaillierPublicKey(n=int(key_data['n']))
    
    @staticmethod
    def serialize_private_key(private_key: paillier.PaillierPrivateKey) -> str:
        """Convert private key to JSON string (in practice, keep this secure!)"""
        return json.dumps({
            'p': private_key.p,
            'q': private_key.q
        })
    
    @staticmethod
    def deserialize_private_key(key_str: str, public_key: paillier.PaillierPublicKey) -> paillier.PaillierPrivateKey:
        """Recreate private key from JSON string"""
        key_data = json.loads(key_str)
        return paillier.PaillierPrivateKey(
            public_key=public_key,
            p=int(key_data['p']),
            q=int(key_data['q'])
        )
    
    @staticmethod
    def encrypt_number(public_key: paillier.PaillierPublicKey, number: float) -> str:
        """Encrypt a single number using the public key"""
        encrypted = public_key.encrypt(number)
        # Serialize to string for transmission
        return json.dumps({
            'ciphertext': str(encrypted.ciphertext()),
            'exponent': encrypted.exponent
        })
    
    @staticmethod
    def decrypt_number(private_key: paillier.PaillierPrivateKey, encrypted_str: str) -> float:
        """Decrypt an encrypted number using the private key"""
        data = json.loads(encrypted_str)
        # Reconstruct EncryptedNumber object
        encrypted_num = paillier.EncryptedNumber(
            public_key=private_key.public_key,
            ciphertext=int(data['ciphertext']),
            exponent=data['exponent']
        )
        return private_key.decrypt(encrypted_num)
    
    @staticmethod
    def add_encrypted_numbers(public_key: paillier.PaillierPublicKey, encrypted_nums: List[str]) -> str:
        """
        Add encrypted numbers without decrypting them.
        This demonstrates homomorphic addition.
        """
        # Deserialize first number
        data = json.loads(encrypted_nums[0])
        result = paillier.EncryptedNumber(
            public_key=public_key,
            ciphertext=int(data['ciphertext']),
            exponent=data['exponent']
        )
        
        # Add remaining numbers
        for encrypted_str in encrypted_nums[1:]:
            data = json.loads(encrypted_str)
            encrypted_num = paillier.EncryptedNumber(
                public_key=public_key,
                ciphertext=int(data['ciphertext']),
                exponent=data['exponent']
            )
            result = result + encrypted_num
        
        # Serialize result
        return json.dumps({
            'ciphertext': str(result.ciphertext()),
            'exponent': result.exponent
        })
    
    @staticmethod
    def multiply_encrypted_by_scalar(public_key: paillier.PaillierPublicKey, 
                                     encrypted_str: str, scalar: float) -> str:
        """
        Multiply an encrypted number by a plaintext scalar.
        This demonstrates homomorphic scalar multiplication.
        """
        data = json.loads(encrypted_str)
        encrypted_num = paillier.EncryptedNumber(
            public_key=public_key,
            ciphertext=int(data['ciphertext']),
            exponent=data['exponent']
        )
        
        # Multiply by scalar
        result = encrypted_num * scalar
        
        return json.dumps({
            'ciphertext': str(result.ciphertext()),
            'exponent': result.exponent
        })