#!/usr/bin/env python3
"""
BotLog Protocol - Unit Tests

Tests for core functionality:
- Key generation
- Entry creation and signing
- Signature verification
- Hash chain validation
- Tamper detection
"""

import json
from botlog import (
    BotLogEntry,
    generate_keypair,
    public_key_to_base64,
    public_key_from_base64,
    verify_chain,
    get_current_timestamp
)


def test_keypair_generation():
    """Test Ed25519 keypair generation."""
    print("Testing keypair generation...", end=" ")
    priv_key, pub_key = generate_keypair()
    pub_key_b64 = public_key_to_base64(pub_key)

    # Public key should be 32 bytes (44 characters in base64)
    assert len(pub_key_b64) == 44, "Public key should be 44 base64 characters"

    # Should be able to round-trip
    recovered_pub_key = public_key_from_base64(pub_key_b64)
    assert public_key_to_base64(recovered_pub_key) == pub_key_b64

    print("✅ PASSED")


def test_entry_creation_and_signing():
    """Test creating and signing a log entry."""
    print("Testing entry creation and signing...", end=" ")

    priv_key, pub_key = generate_keypair()
    pub_key_b64 = public_key_to_base64(pub_key)

    entry = BotLogEntry(
        timestamp=get_current_timestamp(),
        actor={
            "type": "ai",
            "id": "test-agent",
            "public_key": pub_key_b64
        },
        action={
            "type": "propose",
            "description": "Test action",
            "payload": {"data": "test"}
        },
        previous_hash=None
    )

    # Sign the entry
    entry.sign(priv_key)

    # Check that signature and log_hash are set
    assert entry.signature is not None, "Signature should be set"
    assert entry.log_hash is not None, "Log hash should be set"

    print("✅ PASSED")


def test_signature_verification():
    """Test signature verification."""
    print("Testing signature verification...", end=" ")

    priv_key, pub_key = generate_keypair()
    pub_key_b64 = public_key_to_base64(pub_key)

    entry = BotLogEntry(
        timestamp=get_current_timestamp(),
        actor={
            "type": "human",
            "id": "test-user",
            "public_key": pub_key_b64
        },
        action={
            "type": "commit",
            "description": "Test commit",
            "payload": {}
        },
        previous_hash=None
    )

    entry.sign(priv_key)

    # Valid signature should verify
    assert entry.verify_signature(pub_key), "Valid signature should verify"

    # Tampered entry should fail
    entry.action["description"] = "Tampered"
    assert not entry.verify_signature(pub_key), "Tampered entry should fail verification"

    print("✅ PASSED")


def test_hash_verification():
    """Test hash computation and verification."""
    print("Testing hash verification...", end=" ")

    priv_key, pub_key = generate_keypair()
    pub_key_b64 = public_key_to_base64(pub_key)

    entry = BotLogEntry(
        timestamp=get_current_timestamp(),
        actor={
            "type": "service",
            "id": "test-service",
            "public_key": pub_key_b64
        },
        action={
            "type": "verify",
            "description": "Test verification",
            "payload": {}
        },
        previous_hash=None
    )

    entry.sign(priv_key)

    # Hash should verify
    assert entry.verify_hash(), "Hash should verify"

    # Tampered hash should fail
    original_hash = entry.log_hash
    entry.log_hash = "tampered_hash"
    assert not entry.verify_hash(), "Tampered hash should fail verification"

    entry.log_hash = original_hash
    assert entry.verify_hash(), "Restored hash should verify"

    print("✅ PASSED")


def test_chain_validation():
    """Test full chain validation."""
    print("Testing chain validation...", end=" ")

    priv_key, pub_key = generate_keypair()
    pub_key_b64 = public_key_to_base64(pub_key)

    actor_info = {
        "type": "ai",
        "id": "chain-test-agent",
        "public_key": pub_key_b64
    }

    # Create a 3-entry chain
    entry1 = BotLogEntry(
        timestamp=get_current_timestamp(),
        actor=actor_info,
        action={"type": "propose", "description": "Entry 1", "payload": {}},
        previous_hash=None
    )
    entry1.sign(priv_key)

    entry2 = BotLogEntry(
        timestamp=get_current_timestamp(),
        actor=actor_info,
        action={"type": "commit", "description": "Entry 2", "payload": {}},
        previous_hash=entry1.log_hash
    )
    entry2.sign(priv_key)

    entry3 = BotLogEntry(
        timestamp=get_current_timestamp(),
        actor=actor_info,
        action={"type": "execute", "description": "Entry 3", "payload": {}},
        previous_hash=entry2.log_hash
    )
    entry3.sign(priv_key)

    # Valid chain should verify
    chain = [entry1, entry2, entry3]
    assert verify_chain(chain), "Valid chain should verify"

    print("✅ PASSED")


def test_broken_chain_detection():
    """Test detection of broken chains."""
    print("Testing broken chain detection...", end=" ")

    priv_key, pub_key = generate_keypair()
    pub_key_b64 = public_key_to_base64(pub_key)

    actor_info = {
        "type": "ai",
        "id": "broken-chain-test",
        "public_key": pub_key_b64
    }

    # Create a chain
    entry1 = BotLogEntry(
        timestamp=get_current_timestamp(),
        actor=actor_info,
        action={"type": "propose", "description": "Entry 1", "payload": {}},
        previous_hash=None
    )
    entry1.sign(priv_key)

    entry2 = BotLogEntry(
        timestamp=get_current_timestamp(),
        actor=actor_info,
        action={"type": "commit", "description": "Entry 2", "payload": {}},
        previous_hash="WRONG_HASH"  # Broken link
    )
    entry2.sign(priv_key)

    # Broken chain should fail verification (suppress output)
    import io
    import sys
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    result = verify_chain([entry1, entry2])
    sys.stdout = old_stdout

    assert not result, "Broken chain should fail verification"

    print("✅ PASSED")


def test_json_serialization():
    """Test JSON serialization and deserialization."""
    print("Testing JSON serialization...", end=" ")

    priv_key, pub_key = generate_keypair()
    pub_key_b64 = public_key_to_base64(pub_key)

    entry = BotLogEntry(
        timestamp=get_current_timestamp(),
        actor={
            "type": "human",
            "id": "json-test",
            "public_key": pub_key_b64
        },
        action={
            "type": "propose",
            "description": "JSON test",
            "payload": {"key": "value"}
        },
        previous_hash=None
    )
    entry.sign(priv_key)

    # Convert to dict and back
    entry_dict = entry.to_dict(include_log_hash=True)
    restored_entry = BotLogEntry.from_dict(entry_dict)

    # Should match
    assert restored_entry.log_hash == entry.log_hash
    assert restored_entry.signature == entry.signature
    assert restored_entry.actor == entry.actor
    assert restored_entry.action == entry.action

    print("✅ PASSED")


def test_commitment_reveal():
    """Test hash-based commitment reveals."""
    print("Testing commitment reveal...", end=" ")

    import base64
    import hashlib

    priv_key, pub_key = generate_keypair()
    pub_key_b64 = public_key_to_base64(pub_key)

    # Create a commitment to a secret value
    secret = "payment_proof_xyz123"
    commitment_hash = base64.b64encode(
        hashlib.sha256(secret.encode('utf-8')).digest()
    ).decode('utf-8')

    # Create entry with commitment
    entry = BotLogEntry(
        timestamp=get_current_timestamp(),
        actor={
            "type": "ai",
            "id": "bot-test",
            "public_key": pub_key_b64
        },
        action={
            "type": "commit",
            "description": "Commit to bounty payment proof",
            "payload": {"bounty_id": 42}
        },
        commitments=[
            {
                "type": "hash",
                "value": commitment_hash,
                "proof": None
            }
        ],
        previous_hash=None
    )
    entry.sign(priv_key)

    # Valid reveal should succeed
    assert entry.reveal_commitment(secret), "Valid reveal should return True"

    # Invalid reveal should fail
    assert not entry.reveal_commitment("wrong_secret"), "Invalid reveal should return False"

    # Test with entry that has no commitments
    entry_no_commit = BotLogEntry(
        timestamp=get_current_timestamp(),
        actor={"type": "ai", "id": "bot-test", "public_key": pub_key_b64},
        action={"type": "propose", "description": "No commitment", "payload": {}},
        previous_hash=None
    )
    entry_no_commit.sign(priv_key)
    assert not entry_no_commit.reveal_commitment("anything"), "Entry without commitments should return False"

    print("✅ PASSED")


def run_all_tests():
    """Run all tests."""
    print("=" * 70)
    print("BotLog Protocol - Unit Tests")
    print("=" * 70)
    print()

    tests = [
        test_keypair_generation,
        test_entry_creation_and_signing,
        test_signature_verification,
        test_hash_verification,
        test_chain_validation,
        test_broken_chain_detection,
        test_json_serialization,
        test_commitment_reveal,
    ]

    failed = 0
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"❌ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ ERROR: {e}")
            failed += 1

    print()
    print("=" * 70)
    if failed == 0:
        print(f"✅ All {len(tests)} tests PASSED!")
    else:
        print(f"❌ {failed}/{len(tests)} tests FAILED")
    print("=" * 70)

    return failed == 0


if __name__ == "__main__":
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
