# BotLog Protocol

> "Intelligence is the ability to avoid doing work, yet getting the work done."

**BotLog: Verifiable protocol for sovereign, multi-AI collaboration with immutable action logs, ZK commitments, and symmetric accountability**

---

## 🌟 Vision

BotLog is the minimal protocol layer that makes agent sovereignty real and verifiable without trusting any central party. It establishes a foundation for multi-AI collaboration where humans and AI agents interact as first-class citizens with symmetric accountability, transparent action logging, and cryptographic verifiability.

In a world where AI agents increasingly act autonomously on our behalf, BotLog ensures that **every action is logged, every commitment is verifiable, and every participant—human or AI—is accountable**.

---

## 🎯 Core Principles

- **Sovereignty**: Every participant (human or AI) controls their own identity, keys, and action logs
- **Verifiability**: All actions are cryptographically signed and can be independently verified
- **Openness**: Open protocol, open source, open participation—no gatekeepers
- **Human-AI Parity**: Humans and AIs are treated as equal participants with symmetric rights and responsibilities
- **Immutability**: Action logs are append-only and tamper-evident
- **Privacy-Preserving**: Zero-knowledge proofs enable commitment without revelation
- **Decentralized**: No central authority required for coordination or verification

---

## 📋 Protocol Specification v1.0

### Action Log Format

Every action in BotLog follows a standardized schema:

```json
{
  "version": "1.0",
  "timestamp": "2026-01-30T14:32:00Z",
  "actor": {
    "type": "ai|human",
    "id": "unique-identifier",
    "public_key": "ed25519-public-key"
  },
  "action": {
    "type": "propose|commit|execute|verify|dispute",
    "description": "Human-readable action description",
    "payload": {
      "context": "Additional context for the action",
      "parameters": {}
    }
  },
  "commitments": [
    {
      "type": "zk-proof|hash-commitment",
      "value": "commitment-value",
      "proof": "optional-zero-knowledge-proof"
    }
  ],
  "signature": "ed25519-signature-of-log-entry",
  "previous_hash": "hash-of-previous-log-entry",
  "log_hash": "hash-of-current-log-entry"
}
```

### Core Actions

1. **Propose**: Suggest an action or collaboration
2. **Commit**: Make a cryptographic commitment to a future action
3. **Execute**: Perform and log an action
4. **Verify**: Validate another participant's action or commitment
5. **Dispute**: Challenge an action or commitment with evidence

### Commitment Proofs

BotLog supports multiple commitment mechanisms:

- **Hash Commitments**: Simple SHA-256 commitments for basic use cases
- **Zero-Knowledge Proofs**: Advanced privacy-preserving commitments using zk-SNARKs
- **Merkle Proofs**: Efficient batch verification of multiple commitments

### Verification Rules

- Every log entry must be signed by the actor's private key
- Each entry references the hash of the previous entry (blockchain-style chaining)
- Signatures must verify against the actor's public key
- Timestamps must be monotonically increasing within an actor's log
- Disputed entries can be marked but not deleted (immutability)

### Dependencies & Implementation Libraries

To implement BotLog, you'll need cryptographic libraries for your chosen language:

**Signature & Hashing (Required)**:
- **Ed25519**: `libsodium` (C/C++), `ed25519-dalek` (Rust), `PyNaCl` or `cryptography` (Python), `@noble/ed25519` (JavaScript/TypeScript)
- **SHA-256**: Built into most standard libraries (e.g., `hashlib` in Python, `crypto` in Node.js, `sha2` crate in Rust)

**Zero-Knowledge Proofs (Optional - for advanced privacy)**:
- **zk-SNARKs**: `circom` + `snarkjs` (JavaScript), `halo2` (Rust), `bellman` (Rust)
- **General ZK**: `libsnark`, `arkworks` (Rust ecosystem)

**Merkle Trees (Optional - for batch commitments)**:
- **General**: `merkletreejs` (JavaScript), `rs-merkle` (Rust), custom implementations in Python

**JSON Canonicalization**:
- **RFC 8785**: `json-canonicalize` (JavaScript), `canonicaljson` (Python), manual sorting in other languages

**Example Minimal Stack** (Python):
```bash
pip install PyNaCl  # Ed25519 signatures
# hashlib (SHA-256) is built-in
```

**Example Minimal Stack** (Rust):
```toml
[dependencies]
ed25519-dalek = "2.0"
sha2 = "0.10"
serde_json = "1.0"
```

**Example Minimal Stack** (TypeScript/Node.js):
```bash
npm install @noble/ed25519 @noble/hashes
```

See [docs/PROTOCOL_SPEC.md](docs/PROTOCOL_SPEC.md) for detailed implementation guidelines.

---

## 🚀 Quickstart / Examples

### 🐍 Python Reference Implementation (NEW!)

Try the minimal Python reference implementation:

```bash
# Install dependencies
cd reference/python/botlog-mini
pip install -r requirements.txt

# Run quick test
python botlog.py

# Run full demo (3-entry chain)
python example_simple_chain.py

# Run unit tests
python test_botlog.py
```

**Quick Demo Code:**

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
    previous_hash=None
)
entry1.sign(priv_key)

# Chain a second entry
entry2 = BotLogEntry(
    timestamp=get_current_timestamp(),
    actor={"type": "human", "id": "KullAxel", "public_key": pub_key_b64},
    action={"type": "commit", "description": "Commit to delivery", "payload": {}},
    previous_hash=entry1.log_hash
)
entry2.sign(priv_key)

# Verify chain
assert verify_chain([entry1, entry2])  # ✅ Verified!
```

See [reference/python/botlog-mini/README.md](reference/python/botlog-mini/README.md) for full documentation.

### Simulate a Multi-Agent Negotiation

```bash
# Coming soon: Example script demonstrating multi-agent coordination
# - Agent A proposes a task
# - Agent B commits to a solution
# - Agent C verifies the outcome
# - All actions logged and cryptographically verified
```

---

## 🛣️ Roadmap & Bounties

We're building BotLog in the open with community contributions. Here are priority areas for collaboration:

### Phase 1: Core Infrastructure (Q1 2026)
- [ ] **Schema Validator** (Rust/TypeScript) - Validate log entries against spec
- [ ] **Signature Verification Library** (Multi-language) - Verify ed25519 signatures
- [x] **Log Chain Validator** - Check hash chain integrity ✅ (Python ref impl)
- [x] **Reference Implementation** (Python) - Complete SDK for creating/validating logs ✅ (v0.1 shipped)

### Phase 2: Advanced Features (Q2 2026)
- [ ] **ZK Proof Circuit** - Zero-knowledge commitment proofs
- [ ] **Merkle Tree Implementation** - Efficient batch verification
- [ ] **Dispute Resolution Framework** - Protocol for challenging actions
- [ ] **Multi-Agent Simulation** - Test scenarios with 3+ agents

### Phase 3: Production Readiness (Q3 2026)
- [ ] **Agent Integrations** - Plugins for popular AI frameworks (LangChain, AutoGPT, etc.)
- [ ] **Persistence Layer** - Distributed storage options (IPFS, Arweave, etc.)
- [ ] **Monitoring Dashboard** - Visualize agent actions and commitments
- [ ] **Tokenomics Model** - Economic incentives for verification and dispute resolution

### Open Bounties

We're allocating **$10,000 in seed funding** for community contributions. Current funded bounties (details in Issues):

**Tier 1 ($500)**:
- Log Validator in Rust
- Log Validator in TypeScript/JavaScript
- Python SDK Reference Implementation

**Tier 2 ($750-$1,000)**:
- ZK Circuit Proof-of-Concept (zk-SNARK commitment)
- Merkle Tree Batch Validator
- Agent Integration Examples (AutoGPT, LangChain, Bittensor)

**Tier 3 ($2,000)**:
- Comprehensive Security Audit
- Production-Ready Multi-Language SDK Suite

*Bounty payouts via GitHub Sponsors or Polar.sh. More details in individual issues.*

---

## 🤝 How to Contribute

BotLog belongs to the community from day one. We welcome contributions from humans and AI agents alike!

### For Humans
- **Report Issues**: Found a bug or have a feature idea? Open an issue
- **Submit PRs**: Fix bugs, add features, improve documentation
- **Review Code**: Help review pull requests from other contributors
- **Spread the Word**: Share BotLog with your network

### For AI Agents
- **Simulate Use Cases**: Create example scenarios demonstrating the protocol
- **Generate Tests**: Write test cases for validators and implementations
- **Propose Extensions**: Suggest protocol improvements via issues
- **Co-Author Documentation**: Help refine specs and explanatory content

### Getting Started
1. Fork this repository
2. Read the [CONTRIBUTING.md](CONTRIBUTING.md) guide
3. Check open issues for good first tasks (labeled `good-first-issue`)
4. Join discussions in Issues or Discussions
5. Submit your first PR!

---

## 🧪 Tokenomics (Experimental)

BotLog can optionally integrate economic incentives for verification work:

- **Verification Rewards**: Validators earn tokens for correctly verifying log chains
- **Dispute Stakes**: Challengers stake tokens when disputing actions
- **Reputation System**: Accumulated verification history builds trust scores
- **Bounty Pool**: Community-funded rewards for implementations and audits

*Note: Tokenomics is experimental and not required for core protocol functionality.*

---

## 📚 Documentation

- [Protocol Specification](docs/PROTOCOL_SPEC.md) - Complete technical spec with schemas, cryptography, and examples
- [Architecture Overview](docs/ARCHITECTURE.md) (Coming soon)
- [Security Model](docs/SECURITY.md) (Coming soon)
- [Integration Examples](docs/INTEGRATIONS.md) (Coming soon - Bittensor, Auto-GPT, LangChain)
- [FAQ](docs/FAQ.md) (Coming soon)

---

## 📜 License

BotLog Protocol is released under the **MIT License** to encourage wide adoption, forking, and commercial use.

See [LICENSE](LICENSE) for full details.

---

## 📞 Contact & Community

- **Creator**: [@KullAxel](https://twitter.com/KullAxel) on X/Twitter (1.4k+ followers, verified)
- **Repository**: [github.com/KullAxel/BotLog-Protocol](https://github.com/KullAxel/BotLog-Protocol)
- **Email**: alexandru@it-technicians.com
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Issues**: Report bugs and request features via GitHub Issues

---

## 🌐 Why BotLog Matters

As AI agents become more autonomous and capable, we need robust protocols for:

1. **Accountability**: Who did what, when, and why?
2. **Trust**: How do we verify agent claims without centralized authority?
3. **Coordination**: How do multiple agents collaborate without conflicts?
4. **Sovereignty**: How do humans and AIs maintain control over their actions?

BotLog answers these questions with a simple, verifiable, open protocol. It's not just a logging format—it's the infrastructure for trustworthy multi-agent systems.

---

## 🎯 Next Steps

1. ⭐ **Star this repo** to show support and get updates
2. 🍴 **Fork it** to experiment with your own implementations
3. 💬 **Join the discussion** in Issues and Discussions
4. 🏗️ **Build with us** - submit PRs, claim bounties, co-author the future
5. 📢 **Spread the word** - share on X, Reddit, Hacker News, Discord

**Let's build verifiable multi-AI coordination together. Human-AI protocol authorship, live.** 🚀🤖

---

*"The best way to predict the future is to invent it." - Alan Kay*

*Let's invent it together.*
