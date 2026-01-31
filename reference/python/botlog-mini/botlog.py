"""
BotLog Protocol - Minimal Python Reference Implementation
Version: 1.0
Spec: https://github.com/KullAxel/BotLog-Protocol

This minimal implementation demonstrates core BotLog functionality:
- Ed25519 key generation and signing
- SHA-256 hash chaining
- Log entry creation and verification
- Chain integrity validation
"""

import json
import hashlib
import base64
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives import serialization


class BotLogEntry:
    """
    Represents a single entry in a BotLog chain.

    Attributes:
        version: Protocol version (default "1.0")
        timestamp: ISO 8601 UTC timestamp
        actor: Actor information (type, id, public_key)
        action: Action information (type, description, payload)
        commitments: List of cryptographic commitments (optional)
        signature: Ed25519 signature (base64)
        previous_hash: Hash of previous entry (None for genesis)
        log_hash: SHA-256 hash of this entry
    """

    def __init__(
        self,
        timestamp: str,
        actor: Dict[str, str],
        action: Dict[str, Any],
        previous_hash: Optional[str] = None,
        commitments: Optional[List[Dict[str, str]]] = None,
        version: str = "1.0"
    ):
        self.version = version
        self.timestamp = timestamp
        self.actor = actor
        self.action = action
        self.commitments = commitments or []
        self.previous_hash = previous_hash
        self.signature = None
        self.log_hash = None

    def to_dict(self, include_signature: bool = True, include_log_hash: bool = False) -> Dict[str, Any]:
        """Convert entry to dictionary representation."""
        data = {
            "version": self.version,
            "timestamp": self.timestamp,
            "actor": self.actor,
            "action": self.action,
            "commitments": self.commitments,
            "previous_hash": self.previous_hash,
        }

        if include_signature and self.signature:
            data["signature"] = self.signature

        if include_log_hash and self.log_hash:
            data["log_hash"] = self.log_hash

        return data

    def to_canonical_json(self, include_signature: bool = True, include_log_hash: bool = False) -> str:
        """
        Convert entry to canonical JSON for deterministic hashing/signing.

        Canonical JSON rules:
        - Sort object keys alphabetically
        - No whitespace between tokens
        - UTF-8 encoding
        - No trailing commas
        """
        data = self.to_dict(include_signature=include_signature, include_log_hash=include_log_hash)
        return json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False)

    def compute_hash(self) -> str:
        """
        Compute SHA-256 hash of this entry (with signature, without log_hash).
        Returns base64-encoded hash.
        """
        canonical = self.to_canonical_json(include_signature=True, include_log_hash=False)
        hash_bytes = hashlib.sha256(canonical.encode('utf-8')).digest()
        return base64.b64encode(hash_bytes).decode('utf-8')

    def sign(self, private_key: Ed25519PrivateKey) -> None:
        """
        Sign this entry with the provided private key.
        Updates the signature and log_hash fields.
        """
        # Create canonical JSON without signature
        canonical = self.to_canonical_json(include_signature=False)
        message = canonical.encode('utf-8')

        # Sign with Ed25519
        signature_bytes = private_key.sign(message)
        self.signature = base64.b64encode(signature_bytes).decode('utf-8')

        # Compute log hash (includes signature)
        self.log_hash = self.compute_hash()

    def verify_signature(self, public_key: Ed25519PublicKey) -> bool:
        """
        Verify this entry's signature with the provided public key.
        Returns True if valid, False otherwise.
        """
        if not self.signature:
            return False

        try:
            # Reconstruct the signed message (canonical JSON without signature)
            canonical = self.to_canonical_json(include_signature=False)
            message = canonical.encode('utf-8')

            # Decode signature
            signature_bytes = base64.b64decode(self.signature)

            # Verify Ed25519 signature
            public_key.verify(signature_bytes, message)
            return True
        except Exception:
            return False

    def verify_hash(self) -> bool:
        """
        Verify that the log_hash field matches the computed hash.
        Returns True if valid, False otherwise.
        """
        if not self.log_hash:
            return False

        computed = self.compute_hash()
        return self.log_hash == computed

    def reveal_commitment(self, preimage: str, commitment_index: int = 0) -> bool:
        """
        Verify a commitment reveal (hash-based only for v0.1).

        Args:
            preimage: The original value that was hashed
            commitment_index: Index of commitment to verify (default 0)

        Returns:
            True if preimage matches the commitment, False otherwise

        Raises:
            ValueError: If commitment type is not "hash" or "hash-commitment"
        """
        if not self.commitments or commitment_index >= len(self.commitments):
            return False

        commitment = self.commitments[commitment_index]
        commitment_type = commitment.get("type", "")

        if commitment_type not in ["hash", "hash-commitment"]:
            raise ValueError(f"Only hash-commitments supported in v0.1, got: {commitment_type}")

        # Compute hash of preimage
        computed_hash = base64.b64encode(
            hashlib.sha256(preimage.encode('utf-8')).digest()
        ).decode('utf-8')

        return computed_hash == commitment.get("value")

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'BotLogEntry':
        """Create a BotLogEntry from a dictionary."""
        entry = BotLogEntry(
            version=data.get("version", "1.0"),
            timestamp=data["timestamp"],
            actor=data["actor"],
            action=data["action"],
            previous_hash=data.get("previous_hash"),
            commitments=data.get("commitments", [])
        )
        entry.signature = data.get("signature")
        entry.log_hash = data.get("log_hash")
        return entry


def generate_keypair() -> tuple[Ed25519PrivateKey, Ed25519PublicKey]:
    """
    Generate a new Ed25519 keypair.
    Returns (private_key, public_key).
    """
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    return private_key, public_key


def public_key_to_base64(public_key: Ed25519PublicKey) -> str:
    """Convert Ed25519 public key to base64 string."""
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    return base64.b64encode(public_bytes).decode('utf-8')


def public_key_from_base64(public_key_b64: str) -> Ed25519PublicKey:
    """Create Ed25519 public key from base64 string."""
    public_bytes = base64.b64decode(public_key_b64)
    return Ed25519PublicKey.from_public_bytes(public_bytes)


def verify_chain(entries: List[BotLogEntry]) -> bool:
    """
    Verify integrity of a log chain.

    Checks:
    1. Each entry's signature is valid
    2. Each entry's hash is correct
    3. Each entry's previous_hash matches the actual previous entry
    4. Timestamps are monotonically increasing

    Returns True if chain is valid, False otherwise.
    """
    if not entries:
        return True

    for i, entry in enumerate(entries):
        # 1. Verify signature
        try:
            public_key = public_key_from_base64(entry.actor["public_key"])
            if not entry.verify_signature(public_key):
                print(f"❌ Entry {i}: Invalid signature")
                return False
        except Exception as e:
            print(f"❌ Entry {i}: Signature verification error: {e}")
            return False

        # 2. Verify hash
        if not entry.verify_hash():
            print(f"❌ Entry {i}: Hash mismatch")
            return False

        # 3. Verify chain linkage (except genesis)
        if i == 0:
            if entry.previous_hash is not None:
                print(f"❌ Entry {i}: Genesis entry should have previous_hash=None")
                return False
        else:
            previous_entry = entries[i - 1]
            if entry.previous_hash != previous_entry.log_hash:
                print(f"❌ Entry {i}: previous_hash doesn't match previous entry's log_hash")
                return False

        # 4. Verify timestamp ordering
        if i > 0:
            previous_entry = entries[i - 1]
            current_time = datetime.fromisoformat(entry.timestamp.replace('Z', '+00:00'))
            previous_time = datetime.fromisoformat(previous_entry.timestamp.replace('Z', '+00:00'))
            if current_time < previous_time:
                print(f"❌ Entry {i}: Timestamp ordering violation")
                return False

    return True


def get_current_timestamp() -> str:
    """Get current time in ISO 8601 UTC format."""
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


if __name__ == "__main__":
    # Quick test
    print("BotLog Protocol - Minimal Python Reference Implementation")
    print("=" * 60)

    # Generate keypair
    priv_key, pub_key = generate_keypair()
    pub_key_b64 = public_key_to_base64(pub_key)

    print(f"✓ Generated Ed25519 keypair")
    print(f"  Public key: {pub_key_b64[:32]}...")

    # Create a simple entry
    entry = BotLogEntry(
        timestamp=get_current_timestamp(),
        actor={
            "type": "human",
            "id": "KullAxel",
            "public_key": pub_key_b64
        },
        action={
            "type": "propose",
            "description": "Launch BotLog feedback campaign",
            "payload": {}
        },
        previous_hash=None
    )

    # Sign it
    entry.sign(priv_key)

    print(f"✓ Created and signed entry")
    print(f"  Hash: {entry.log_hash[:32]}...")

    # Verify it
    if entry.verify_signature(pub_key) and entry.verify_hash():
        print(f"✓ Signature and hash verified!")
    else:
        print(f"❌ Verification failed!")

    # Print JSON
    print("\nEntry JSON:")
    print(json.dumps(entry.to_dict(include_log_hash=True), indent=2))
