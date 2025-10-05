from fastapi import APIRouter, HTTPException
from app.models import (
    EncryptRequest, EncryptResponse,
    ComputeRequest, ComputeResponse,
    DecryptRequest, DecryptResponse
)
from app.encryption import HomomorphicEncryption

router = APIRouter()

temp_keypair_storage = {}

@router.post("/encrypt", response_model=EncryptResponse, tags=["Encryption"])
async def encrypt_numbers(request: EncryptRequest):
    """
    Encrypt a list of numbers using Paillier homomorphic encryption.
    Returns encrypted values, public key, and private key (for testing).
    """
    try:
        # Generate new keypair
        public_key, private_key = HomomorphicEncryption.generate_keypair()
        
        # Encrypt each number
        encrypted_numbers = [
            HomomorphicEncryption.encrypt_number(public_key, num)
            for num in request.numbers
        ]
        
        # Serialize keys
        public_key_str = HomomorphicEncryption.serialize_public_key(public_key)
        private_key_str = HomomorphicEncryption.serialize_private_key(private_key)
        
        temp_keypair_storage[public_key_str] = private_key_str
        
        return EncryptResponse(
            encrypted_numbers=encrypted_numbers,
            public_key=public_key_str,
            private_key=private_key_str 
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Encryption failed: {str(e)}")
@router.post("/compute", response_model=ComputeResponse, tags=["Homomorphic Operations"])
async def compute_on_encrypted(request: ComputeRequest):
    """
    Perform computations on encrypted data without decrypting.
    Supports 'add' (addition) and 'multiply' (scalar multiplication).
    """
    try:
        # Deserialize public key
        public_key = HomomorphicEncryption.deserialize_public_key(request.public_key)
        
        operation = request.operation.lower()
        
        if operation in ["add", "sum"]:
            # Add all encrypted numbers together
            result = HomomorphicEncryption.add_encrypted_numbers(
                public_key, 
                request.encrypted_numbers
            )
        elif operation == "multiply":
            if request.multiplier is None:
                raise HTTPException(
                    status_code=400, 
                    detail="Multiplier required for multiply operation"
                )
            result = HomomorphicEncryption.multiply_encrypted_by_scalar(
                public_key,
                request.encrypted_numbers[0],
                request.multiplier
            )
        else:
            raise HTTPException(
                status_code=400, 
                detail="Invalid operation. Use 'add', 'sum', or 'multiply'"
            )
        
        return ComputeResponse(encrypted_result=result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Computation failed: {str(e)}")

@router.post("/decrypt", response_model=DecryptResponse, tags=["Decryption"])
async def decrypt_value(request: DecryptRequest):
    """
    Decrypt an encrypted value using the private key.
    """
    try:
        private_key_str = request.private_key
        
        import json
        priv_data = json.loads(private_key_str)
        
        # Reconstruct public key (n = p * q)
        n = priv_data['p'] * priv_data['q']
        public_key_str = json.dumps({'n': n})
        
        public_key = HomomorphicEncryption.deserialize_public_key(public_key_str)
        private_key = HomomorphicEncryption.deserialize_private_key(
            private_key_str, 
            public_key
        )
        
        # Decrypt the value
        decrypted = HomomorphicEncryption.decrypt_number(
            private_key, 
            request.encrypted_value
        )
        
        return DecryptResponse(decrypted_value=decrypted)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Decryption failed: {str(e)}")

@router.get("/demo/full-workflow", tags=["Demo"])
async def demo_full_workflow():
    """
    Demonstrates a complete homomorphic encryption workflow:
    1. Encrypt numbers [10, 20, 30]
    2. Sum them while encrypted
    3. Decrypt the result (should be 60)
    """
    try:
        public_key, private_key = HomomorphicEncryption.generate_keypair()
        numbers = [10, 20, 30]
        
        encrypted = [
            HomomorphicEncryption.encrypt_number(public_key, num)
            for num in numbers
        ]
        
        encrypted_sum = HomomorphicEncryption.add_encrypted_numbers(
            public_key, 
            encrypted
        )
        
        decrypted_sum = HomomorphicEncryption.decrypt_number(
            private_key, 
            encrypted_sum
        )
        
        return {
            "original_numbers": numbers,
            "expected_sum": sum(numbers),
            "computed_sum": decrypted_sum,
            "verification": "✓ Success" if abs(decrypted_sum - sum(numbers)) < 0.01 else "✗ Failed"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Demo failed: {str(e)}")