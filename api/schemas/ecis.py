from pydantic import BaseModel, Field


class EcisPublicKey(BaseModel):
    """
    Model for ECIS public key.
    """

    key: str = Field(..., description="Public key in PEM format.")
    sha3_512: str = Field(..., description="SHA3-512 hash of the public key.")
    request_time: str = Field(..., description="Time of the request in ISO format.")
