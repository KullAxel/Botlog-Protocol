# BotLog Protocol - Python Reference Implementation

A minimal, runnable Python implementation of the BotLog Protocol v1.0. This reference demonstrates core functionality: Ed25519 signing, SHA-256 hash chaining, and verifiable log chains.

## Features

✅ **Ed25519 Signatures** - Cryptographic proof of authorship
✅ **SHA-256 Hash Chains** - Tamper-evident linked entries
✅ **Chain Verification** - Validate signatures and integrity
✅ **Action Types** - Propose, commit, execute, verify, dispute
✅ **Canonical JSON** - Deterministic serialization
✅ **Zero Dependencies** - Only uses Python stdlib + `cryptography`

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run quick test
python botlog.py
```

### Quick Demo

```python
from botlog import BotLogEntry, generate_keypair, public_key_to_base64, verify_chain, get_current_timestamp

# Generate keypair
priv_key, pub_key = generate_keypair()
pub_key_b64 = public_key_to_base64(pub_key)

# Create genesis entry
entry1 = BotLogEntry(
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
    prev_hash=None
)
entry1.sign(priv_key)

# Create linked entry
entry2 = BotLogEntry(
    timestamp=get_current_timestamp(),
    actor={"type": "human", "id": "KullAxel", "public_key": pub_key_b64},
    action={"type": "commit", "description": "Commit to delivery", "payload": {}},
    previous_hash=entry1.log_hash
)
entry2.sign(priv_key)

# Verify chain
assert verify_chain([entry1, entry2])  # ✅ True
```

## Examples

### Run Full Chain Demo

```bash
python example_simple_chain.py
```

This demonstrates:
- Generating Ed25519 keypairs
- Creating a 3-entry chain (propose → commit → execute)
- Verifying signatures and chain integrity
- Detecting tampering attempts

### Run Tests

```bash
python test_botlog.py
```

Runs 7 unit tests covering:
- Keypair generation
- Entry creation and signing
- Signature verification
- Hash verification
- Chain validation
- Broken chain detection
- JSON serialization

## Core API

### Key Generation

```python
from botlog import generate_keypair, public_key_to_base64

priv_key, pub_key = generate_keypair()
pub_key_b64 = public_key_to_base64(pub_key)
```

### Create Entry

```python
from botlog import BotLogEntry, get_current_timestamp

entry = BotLogEntry(
    timestamp=get_current_timestamp(),
    actor={"type": "ai", "id": "agent-1", "public_key": "<base64-pubkey>"},
    action={"type": "propose", "description": "Do something", "payload": {}},
    previous_hash=None  # or previous entry's log_hash
)
```

### Sign Entry

```python
entry.sign(private_key)  # Sets entry.signature and entry.log_hash
```

### Verify Entry

```python
# Verify signature
is_valid = entry.verify_signature(public_key)

# Verify hash
is_valid = entry.verify_hash()
```

### Verify Chain

```python
from botlog import verify_chain

chain = [entry1, entry2, entry3]
is_valid = verify_chain(chain)  # Checks all entries + linkage
```

## File Structure

```
botlog-mini/
├── botlog.py                 # Core implementation
├── example_simple_chain.py   # Full demo (3-entry chain)
├── test_botlog.py            # Unit tests
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

## How It Works

1. **Entry Creation**: Create a `BotLogEntry` with timestamp, actor, and action
2. **Signing**: Call `entry.sign(private_key)` to:
   - Create canonical JSON (sorted keys, no whitespace)
   - Sign with Ed25519
   - Compute SHA-256 hash (includes signature)
3. **Chaining**: Set next entry's `previous_hash` to current entry's `log_hash`
4. **Verification**: Call `verify_chain()` to check:
   - All signatures are valid
   - All hashes are correct
   - Chain linkage is intact
   - Timestamps are ordered

## Specification Compliance

This implementation follows [BotLog Protocol Specification v1.0](../../../docs/PROTOCOL_SPEC.md):

- ✅ Ed25519 signatures (RFC 8032)
- ✅ SHA-256 hashing (FIPS 180-4)
- ✅ Canonical JSON (RFC 8785 principles)
- ✅ Action types: propose, commit, execute, verify, dispute
- ✅ Chain integrity rules
- ⚠️ Commitments: Hash commitments supported (ZK proofs not yet implemented)

## Limitations

This is a **minimal reference implementation** for demonstration purposes:

- ❌ No network transport
- ❌ No persistence layer
- ❌ No ZK proof support (yet)
- ❌ No multi-signature actions (yet)
- ❌ No commitment reveals implementation

For production use, consider adding:
- Persistent storage (SQLite, PostgreSQL, etc.)
- Network sync (HTTP, P2P gossip)
- Advanced commitments (Merkle trees, ZK-SNARKs)
- Dispute resolution mechanisms

## Next Steps

1. **Extend**: Add ZK proof commitments
2. **Integrate**: Build storage backends (SQLite, IPFS)
3. **Network**: Implement P2P log sharing
4. **Test**: Add more edge cases and fuzzing
5. **Optimize**: Profile and optimize for larger chains

## Contributing

This reference implementation is part of the BotLog Protocol project. Contributions welcome!

See [CONTRIBUTING.md](../../../CONTRIBUTING.md) for bounties and contribution guidelines.

## License

MIT License - See [LICENSE](../../../LICENSE)

---

**BotLog Protocol**: Verifiable coordination for the multi-agent era.
**GitHub**: https://github.com/KullAxel/BotLog-Protocol
