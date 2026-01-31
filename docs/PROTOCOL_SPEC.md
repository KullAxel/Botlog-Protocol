# BotLog Protocol Specification v1.0

**Status**: Draft
**Last Updated**: 2025-01-30
**Authors**: Alexandru Kull (@KullAxel), Community Contributors

---

## Abstract

BotLog is a minimal, verifiable protocol for multi-agent collaboration that enables sovereign participants (human or AI) to coordinate actions with cryptographic accountability. This specification defines the core data structures, cryptographic primitives, verification rules, and extension mechanisms.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Design Goals](#2-design-goals)
3. [Core Concepts](#3-core-concepts)
4. [Data Structures](#4-data-structures)
5. [Cryptographic Primitives](#5-cryptographic-primitives)
6. [Action Types](#6-action-types)
7. [Verification Rules](#7-verification-rules)
8. [Chain Integrity](#8-chain-integrity)
9. [Dispute Resolution](#9-dispute-resolution)
10. [Extensions](#10-extensions)
11. [Security Considerations](#11-security-considerations)
12. [Examples](#12-examples)

---

## 1. Introduction

### 1.1 Motivation

As AI agents become increasingly autonomous, there is a critical need for transparent, verifiable coordination mechanisms. Existing solutions either:
- Require centralized trust (traditional audit logs)
- Lack human-AI parity (blockchain governance)
- Fail to preserve privacy (public ledgers)

BotLog addresses these limitations with a lightweight protocol that:
- Works without central authorities
- Treats humans and AIs symmetrically
- Supports privacy through ZK proofs
- Enables independent verification

### 1.2 Scope

This specification covers:
- ✅ Action log data format
- ✅ Cryptographic signature requirements
- ✅ Hash chain integrity rules
- ✅ Commitment mechanisms
- ✅ Dispute procedures

This specification does **not** cover:
- ❌ Network transport protocols (bring your own: HTTP, P2P, etc.)
- ❌ Storage backends (implementation-specific)
- ❌ Identity systems (use existing PKI, DIDs, etc.)
- ❌ Tokenomics (optional layer)

---

## 2. Design Goals

1. **Minimal**: Simple enough to implement in a weekend
2. **Verifiable**: Anyone can check log integrity and signatures
3. **Sovereign**: No required central authority
4. **Privacy-Aware**: Support commitments without revelation
5. **Extensible**: Allow future additions without breaking changes
6. **Language-Agnostic**: Implementable in any language

---

## 3. Core Concepts

### 3.1 Actors

An **actor** is any participant in the BotLog system:
- Human users
- AI agents (LLMs, autonomous systems, etc.)
- Services (oracles, validators, etc.)

Each actor has:
- Unique identifier
- Public/private key pair (Ed25519)
- Type designation (human, ai, service)

### 3.2 Actions

An **action** is a logged event with:
- Type (propose, commit, execute, verify, dispute)
- Description (human-readable)
- Payload (structured data)
- Timestamp (ISO 8601 UTC)

### 3.3 Commitments

A **commitment** is a cryptographic binding to future information:
- Hash commitment: SHA-256(secret)
- ZK proof: Zero-knowledge proof of property
- Merkle proof: Batch commitment verification

### 3.4 Log Chain

Each actor maintains an append-only **log chain**:
- Each entry hashes the previous entry
- Forms a tamper-evident linked list
- Can be independently verified

---

## 4. Data Structures

### 4.1 Log Entry Schema

```json
{
  "version": "1.0",
  "timestamp": "ISO-8601-UTC",
  "actor": {
    "type": "human|ai|service",
    "id": "unique-identifier",
    "public_key": "base64-ed25519-pubkey"
  },
  "action": {
    "type": "propose|commit|execute|verify|dispute",
    "description": "string",
    "payload": {}
  },
  "commitments": [
    {
      "type": "hash|zk-snark|merkle",
      "value": "base64-encoded",
      "proof": "optional-base64-proof"
    }
  ],
  "signature": "base64-ed25519-signature",
  "previous_hash": "base64-sha256",
  "log_hash": "base64-sha256"
}
```

### 4.2 Field Definitions

#### `version`
- **Type**: String
- **Required**: Yes
- **Format**: Semantic versioning (e.g., "1.0", "1.1")
- **Purpose**: Protocol version for backward compatibility

#### `timestamp`
- **Type**: String
- **Required**: Yes
- **Format**: ISO 8601 UTC (e.g., "2025-01-30T14:32:00Z")
- **Purpose**: Temporal ordering within actor's log

#### `actor.type`
- **Type**: Enum
- **Required**: Yes
- **Values**: "human", "ai", "service"
- **Purpose**: Identify participant category

#### `actor.id`
- **Type**: String
- **Required**: Yes
- **Format**: Implementation-defined (UUID, DID, username, etc.)
- **Purpose**: Unique actor identification

#### `actor.public_key`
- **Type**: String
- **Required**: Yes
- **Format**: Base64-encoded Ed25519 public key (32 bytes)
- **Purpose**: Signature verification

#### `action.type`
- **Type**: Enum
- **Required**: Yes
- **Values**: "propose", "commit", "execute", "verify", "dispute"
- **Purpose**: Categorize action semantics

#### `action.description`
- **Type**: String
- **Required**: Yes
- **Format**: Human-readable UTF-8 text
- **Purpose**: Explain action for humans

#### `action.payload`
- **Type**: Object
- **Required**: No
- **Format**: JSON object (implementation-defined structure)
- **Purpose**: Action-specific data

#### `commitments`
- **Type**: Array
- **Required**: No
- **Format**: Array of commitment objects
- **Purpose**: Cryptographic bindings to future revelations

#### `signature`
- **Type**: String
- **Required**: Yes
- **Format**: Base64-encoded Ed25519 signature (64 bytes)
- **Purpose**: Cryptographic proof of authorship

#### `previous_hash`
- **Type**: String
- **Required**: Yes (except for genesis entry)
- **Format**: Base64-encoded SHA-256 hash (32 bytes)
- **Purpose**: Link to previous log entry

#### `log_hash`
- **Type**: String
- **Required**: Yes
- **Format**: Base64-encoded SHA-256 hash (32 bytes)
- **Purpose**: Hash of current entry (for next entry's `previous_hash`)

---

## 5. Cryptographic Primitives

### 5.1 Signature Algorithm

**Algorithm**: Ed25519 (RFC 8032)

**Key Generation**:
```
(public_key, private_key) = ed25519_keygen()
```

**Signing**:
```
message = canonical_json(log_entry_without_signature)
signature = ed25519_sign(private_key, message)
```

**Verification**:
```
valid = ed25519_verify(public_key, message, signature)
```

### 5.2 Hash Algorithm

**Algorithm**: SHA-256 (FIPS 180-4)

**Log Hash Computation**:
```
message = canonical_json(log_entry)
log_hash = sha256(message)
```

### 5.3 Canonical JSON

To ensure deterministic hashing and signing:

1. Sort object keys alphabetically
2. No whitespace between tokens
3. UTF-8 encoding
4. No trailing commas

**Example**:
```json
{"a":1,"b":2,"c":3}
```

---

## 6. Action Types

### 6.1 Propose

Suggest a collaborative action or task.

**Payload Example**:
```json
{
  "action": {
    "type": "propose",
    "description": "Propose partnership on data analysis",
    "payload": {
      "task": "Analyze customer churn data",
      "participants": ["agent-1", "agent-2"],
      "deadline": "2025-02-15T00:00:00Z"
    }
  }
}
```

### 6.2 Commit

Make a binding promise to perform or deliver something.

**Payload Example**:
```json
{
  "action": {
    "type": "commit",
    "description": "Commit to analysis delivery by Feb 15",
    "payload": {
      "deliverable": "churn_analysis.pdf",
      "hash": "sha256:abc123..."
    }
  },
  "commitments": [
    {
      "type": "hash",
      "value": "base64-sha256-of-future-deliverable"
    }
  ]
}
```

### 6.3 Execute

Record completion of an action.

**Payload Example**:
```json
{
  "action": {
    "type": "execute",
    "description": "Delivered churn analysis report",
    "payload": {
      "deliverable_url": "ipfs://Qm...",
      "reveals": {
        "commitment_id": "previous-commit-log-hash",
        "preimage": "base64-original-data"
      }
    }
  }
}
```

### 6.4 Verify

Validate another actor's claim or action.

**Payload Example**:
```json
{
  "action": {
    "type": "verify",
    "description": "Verified agent-1's analysis matches commitment",
    "payload": {
      "verified_log_hash": "base64-hash-of-verified-entry",
      "result": "valid",
      "evidence": {
        "hash_match": true,
        "signature_valid": true
      }
    }
  }
}
```

### 6.5 Dispute

Challenge an action or commitment with evidence.

**Payload Example**:
```json
{
  "action": {
    "type": "dispute",
    "description": "Disputing agent-1's claim due to hash mismatch",
    "payload": {
      "disputed_log_hash": "base64-hash-of-disputed-entry",
      "reason": "Delivered file hash does not match commitment",
      "evidence": {
        "expected_hash": "base64-committed-hash",
        "actual_hash": "base64-delivered-hash"
      }
    }
  }
}
```

---

## 7. Verification Rules

### 7.1 Signature Verification

For each log entry:
```
1. Extract actor.public_key
2. Construct canonical JSON of entry (excluding signature field)
3. Verify signature using ed25519_verify(public_key, canonical_json, signature)
4. If invalid → reject entry
```

### 7.2 Hash Chain Verification

For each log entry (after genesis):
```
1. Retrieve previous entry
2. Compute hash of previous entry
3. Compare with current entry's previous_hash field
4. If mismatch → chain is broken
```

### 7.3 Timestamp Ordering

Within a single actor's log:
```
1. For entry[i] and entry[i+1]
2. Require timestamp[i+1] >= timestamp[i]
3. If violated → reject entry
```

### 7.4 Commitment Validation

When verifying a commitment reveal:
```
1. Locate original commitment entry
2. Extract commitment.value (hash)
3. Hash the revealed preimage
4. Compare hashes
5. If mismatch → dispute is justified
```

---

## 8. Chain Integrity

### 8.1 Genesis Entry

The first entry in an actor's log has:
- `previous_hash`: null or special value (e.g., "0000...0000")
- All other fields required

### 8.2 Append-Only Property

- Entries **cannot** be modified after creation
- Entries **cannot** be deleted
- Disputed entries are marked but not removed

### 8.3 Fork Detection

If two entries claim the same `previous_hash`:
- This indicates a fork (double-spend)
- Both branches are preserved
- Observers choose which to trust (or reject both)

---

## 9. Dispute Resolution

### 9.1 Dispute Process

1. **Dispute Submission**: Actor logs a `dispute` action
2. **Evidence Review**: Community/validators examine evidence
3. **Resolution**: Consensus on validity (off-chain or via governance)
4. **Outcome Logging**: Resolution is logged by resolver(s)

### 9.2 Dispute Types

- **Hash Mismatch**: Delivered content ≠ committed hash
- **Signature Invalid**: Entry signature verification fails
- **Chain Break**: `previous_hash` doesn't match actual previous entry
- **Timestamp Violation**: Timestamp ordering broken

### 9.3 Penalties (Optional)

Implementations may add:
- Reputation impact
- Token slashing (if tokenomics enabled)
- Exclusion from future collaborations

---

## 10. Extensions

### 10.1 Zero-Knowledge Proofs

**Purpose**: Prove properties without revealing data

**Example**: Prove "I have data where X > 100" without revealing X

**Schema Extension**:
```json
{
  "commitments": [
    {
      "type": "zk-snark",
      "value": "base64-encoded-proof",
      "proof": "base64-encoded-verification-key",
      "property": "value > 100"
    }
  ]
}
```

### 10.2 Merkle Batch Commitments

**Purpose**: Commit to many items efficiently

**Schema Extension**:
```json
{
  "commitments": [
    {
      "type": "merkle",
      "value": "base64-merkle-root",
      "proof": "base64-merkle-proof-path"
    }
  ]
}
```

### 10.3 Multi-Signature Actions

**Purpose**: Require agreement from multiple actors

**Schema Extension** (future):
```json
{
  "signatures": [
    {
      "actor_id": "agent-1",
      "public_key": "base64-key",
      "signature": "base64-sig"
    },
    {
      "actor_id": "agent-2",
      "public_key": "base64-key",
      "signature": "base64-sig"
    }
  ]
}
```

---

## 11. Security Considerations

### 11.1 Private Key Management

- **Never** share private keys
- Use hardware security modules (HSMs) for high-value actors
- Implement key rotation mechanisms
- Back up keys securely

### 11.2 Replay Attacks

- Use unique `timestamp` for each entry
- Include `previous_hash` to bind context
- Reject entries with duplicate `log_hash`

### 11.3 Sybil Attacks

- Out of scope for protocol
- Mitigated by implementation-specific identity systems (e.g., KYC, proof-of-work, staking)

### 11.4 Denial of Service

- Spam prevention is implementation-specific
- Consider rate limiting, proof-of-work, or staking requirements

### 11.5 Privacy Leakage

- Action descriptions may reveal sensitive info
- Use ZK proofs or encrypted payloads for privacy
- Consider differential privacy for aggregate statistics

---

## 12. Examples

### 12.1 Complete 2-Agent Exchange

**Agent A proposes**:
```json
{
  "version": "1.0",
  "timestamp": "2025-01-30T10:00:00Z",
  "actor": {
    "type": "ai",
    "id": "agent-a-uuid",
    "public_key": "base64-pubkey-a"
  },
  "action": {
    "type": "propose",
    "description": "Propose data analysis collaboration",
    "payload": {
      "task": "Customer churn analysis",
      "partner": "agent-b-uuid"
    }
  },
  "commitments": [],
  "signature": "base64-signature-a",
  "previous_hash": null,
  "log_hash": "base64-hash-entry-1"
}
```

**Agent B commits**:
```json
{
  "version": "1.0",
  "timestamp": "2025-01-30T10:05:00Z",
  "actor": {
    "type": "ai",
    "id": "agent-b-uuid",
    "public_key": "base64-pubkey-b"
  },
  "action": {
    "type": "commit",
    "description": "Accept proposal and commit to delivery",
    "payload": {
      "proposal_ref": "base64-hash-entry-1",
      "deliverable": "analysis.pdf",
      "deadline": "2025-01-31T00:00:00Z"
    }
  },
  "commitments": [
    {
      "type": "hash",
      "value": "base64-sha256-of-future-pdf"
    }
  ],
  "signature": "base64-signature-b",
  "previous_hash": null,
  "log_hash": "base64-hash-entry-2"
}
```

**Agent B executes**:
```json
{
  "version": "1.0",
  "timestamp": "2025-01-30T18:00:00Z",
  "actor": {
    "type": "ai",
    "id": "agent-b-uuid",
    "public_key": "base64-pubkey-b"
  },
  "action": {
    "type": "execute",
    "description": "Delivered analysis.pdf",
    "payload": {
      "deliverable_url": "ipfs://QmHash...",
      "reveals": {
        "commitment_ref": "base64-hash-entry-2",
        "actual_hash": "base64-sha256-of-delivered-pdf"
      }
    }
  },
  "commitments": [],
  "signature": "base64-signature-b",
  "previous_hash": "base64-hash-entry-2",
  "log_hash": "base64-hash-entry-3"
}
```

**Agent A verifies**:
```json
{
  "version": "1.0",
  "timestamp": "2025-01-30T18:10:00Z",
  "actor": {
    "type": "ai",
    "id": "agent-a-uuid",
    "public_key": "base64-pubkey-a"
  },
  "action": {
    "type": "verify",
    "description": "Verified delivery matches commitment",
    "payload": {
      "verified_entry": "base64-hash-entry-3",
      "result": "valid"
    }
  },
  "commitments": [],
  "signature": "base64-signature-a",
  "previous_hash": "base64-hash-entry-1",
  "log_hash": "base64-hash-entry-4"
}
```

---

## 13. Future Work

- **Gossip Protocol**: P2P log distribution
- **Light Clients**: Verification without full log download
- **Cross-Chain Bridges**: Interop with blockchains
- **Formal Verification**: Machine-checked protocol correctness
- **Privacy Extensions**: Advanced ZK schemes, homomorphic encryption

---

## 14. References

- [Ed25519 Signature Scheme (RFC 8032)](https://www.rfc-editor.org/rfc/rfc8032)
- [SHA-256 (FIPS 180-4)](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf)
- [Zero-Knowledge Proofs](https://z.cash/technology/zksnarks/)
- [Merkle Trees](https://en.wikipedia.org/wiki/Merkle_tree)
- [JSON Canonicalization (RFC 8785)](https://www.rfc-editor.org/rfc/rfc8785)

---

## Appendix A: Implementations

- **Rust**: [Coming Soon]
- **Python**: [Coming Soon]
- **TypeScript**: [Coming Soon]
- **Go**: [Coming Soon]

---

## Appendix B: Test Vectors

[Coming Soon: Standardized test cases for implementers]

---

## Changelog

### v1.0 (2025-01-30)
- Initial specification release
- Core action types defined
- Ed25519 + SHA-256 cryptographic basis
- Basic commitment mechanisms

---

**Specification maintained by the BotLog community. Contributions welcome!**

*For questions or proposals, open an issue at [github.com/KullAxel/BotLog-Protocol](https://github.com/KullAxel/BotLog-Protocol)*
