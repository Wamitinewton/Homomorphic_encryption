from pydantic import BaseModel, Field
from typing import List, Optional

class EncryptRequest(BaseModel):
    """Request model for encrypting numbers"""
    numbers: List[float] = Field(..., description="List of numbers to encrypt")
    
    class Config:
        json_schema_extra = {
            "example": {
                "numbers": [10, 20, 30]
            }
        }

class EncryptResponse(BaseModel):
    """Response model containing encrypted values and keys"""
    encrypted_numbers: List[str] = Field(..., description="Encrypted numbers as JSON strings")
    public_key: str = Field(..., description="Public key for operations")
    private_key: str = Field(..., description="Private key for decryption")
    
    class Config:
        json_schema_extra = {
            "example": {
                "encrypted_numbers": [
                    "{\"ciphertext\": \"123...\", \"exponent\": 0}",
                    "{\"ciphertext\": \"456...\", \"exponent\": 0}"
                ],
                "public_key": "{\"n\": 789...}",
                "private_key": "{\"p\": 123..., \"q\": 456...}"
            }
        }

class ComputeRequest(BaseModel):
    """Request model for computing on encrypted data"""
    encrypted_numbers: List[str] = Field(..., description="Encrypted numbers (JSON format from /encrypt)")
    public_key: str = Field(..., description="Public key used for encryption")
    operation: str = Field(..., description="Operation: 'add', 'sum', or 'multiply'")
    multiplier: Optional[float] = Field(None, description="Multiplier for multiply operation")
    
    class Config:
        json_schema_extra = {
            "example": {
                "encrypted_numbers": [
                    "{\"ciphertext\": \"123...\", \"exponent\": 0}",
                    "{\"ciphertext\": \"456...\", \"exponent\": 0}"
                ],
                "public_key": "{\"n\": 789...}",
                "operation": "add"
            }
        }

class ComputeResponse(BaseModel):
    """Response model for computation result"""
    encrypted_result: str = Field(..., description="Encrypted computation result (JSON format)")

class DecryptRequest(BaseModel):
    """Request model for decrypting values"""
    encrypted_value: str = Field(..., description="Encrypted value (JSON format)")
    private_key: str = Field(..., description="Private key for decryption")

class DecryptResponse(BaseModel):
    """Response model for decrypted value"""
    decrypted_value: float = Field(..., description="Decrypted result")