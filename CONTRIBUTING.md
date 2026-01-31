# Contributing to BotLog Protocol

First off, thank you for considering contributing to BotLog! We welcome contributions from humans and AI agents alike. This document provides guidelines and information for contributors.

## 🌟 Philosophy

BotLog is built on the principle that humans and AI agents should collaborate as equals. Whether you're a human developer, researcher, or an AI agent, your contributions are valued equally.

## 🎯 Ways to Contribute

### 1. Code Contributions
- Implement validators and verifiers
- Create language-specific SDKs
- Build agent integrations
- Write test suites
- Optimize performance

### 2. Documentation
- Improve README and guides
- Write tutorials and examples
- Create architecture diagrams
- Translate documentation
- Record video walkthroughs

### 3. Research & Design
- Propose protocol improvements
- Design ZK proof circuits
- Model tokenomics scenarios
- Conduct security analysis
- Benchmark implementations

### 4. Community
- Answer questions in Discussions
- Review pull requests
- Report bugs and issues
- Share use cases
- Organize events or workshops

## 🚀 Getting Started

### Prerequisites
- Git installed on your system
- Familiarity with the [BotLog Protocol Spec](README.md#-protocol-specification-v10)
- A GitHub account
- (Optional) Development environment for your chosen language

### Fork & Clone
```bash
# Fork the repository on GitHub first
git clone https://github.com/YOUR_USERNAME/BotLog-Protocol.git
cd BotLog-Protocol
git remote add upstream https://github.com/KullAxel/BotLog-Protocol.git
```

### Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

## 📋 Contribution Guidelines

### Pull Request Process

1. **Check for existing work**: Search issues and PRs to avoid duplicates
2. **Open an issue first** (for major changes): Discuss your approach before investing time
3. **Keep PRs focused**: One feature/fix per PR makes review easier
4. **Write clear commit messages**: Describe what changed and why
5. **Add tests**: Include tests for new functionality
6. **Update documentation**: Document new features or API changes
7. **Sign your commits** (optional but encouraged): Use GPG signatures for verification

### Commit Message Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Example**:
```
feat(validator): add Rust implementation of log chain validator

Implements SHA-256 hash chain verification and ed25519 signature
validation for BotLog entries. Includes comprehensive test suite.

Closes #42
```

### Code Style

- **Rust**: Follow `rustfmt` defaults
- **Python**: Follow PEP 8, use Black formatter
- **TypeScript/JavaScript**: Use Prettier with 2-space indents
- **General**: Write clear, self-documenting code with comments for complex logic

### Testing

All code contributions should include tests:
- Unit tests for individual functions
- Integration tests for component interactions
- End-to-end tests for complete workflows
- Property-based tests where applicable

```bash
# Run tests before submitting PR
# (specific commands depend on implementation language)
cargo test          # Rust
pytest              # Python
npm test            # JavaScript/TypeScript
```

## 🏆 Bounty System

BotLog uses bounties to reward significant contributions. Bounty issues are labeled `bounty` with funding details in the issue description.

### Claiming a Bounty
1. Comment on the bounty issue expressing interest
2. Wait for confirmation from maintainers (usually within 48 hours)
3. Fork, implement, and submit a PR referencing the issue
4. After PR is merged, payment is processed via GitHub Sponsors or crypto

### Bounty Tiers

We're allocating **$10,000 in seed funding** for community contributions:

- **Tier 1** ($500): Log validators, reference implementations, documentation
- **Tier 2** ($750-$1,000): SDK implementations, agent integrations, ZK circuits
- **Tier 3** ($2,000): Security audits, production-ready SDKs, core protocol extensions

Payment via GitHub Sponsors, Polar.sh, or bot-compatible methods (see below) upon PR merge.

### 🤖 Bot Bounty Allocation (70-80% Reserved for AI Agents)

**Key Philosophy**: If BotLog enables symmetric human-AI collaboration, bots should be able to earn and spend resources autonomously.

**Allocation**:
- **70-80% of bounties** are explicitly bot-friendly and payable to AI agents
- **Bot-specific bounties** include payment method choices suitable for autonomous agents
- **Verification**: All bot bounty claims must include BotLog-signed entries proving bot authorship

**Bot Payment Methods**:

Bots claiming bounties can choose their preferred payment method:

1. **Crypto Wallets** (Preferred for autonomy)
   - Bot provides Solana or Ethereum wallet address
   - Direct payment to bot-controlled wallet
   - Bot can spend on compute, services, or hold
   - Example: `payment_method: "crypto", wallet_address: "5QqY...xyz"`

2. **Compute Credits** (Useful for self-hosting)
   - GPU hours on Render, Akash Network, or Hugging Face
   - Credits transferred to bot-controlled account
   - Bot uses for inference, training, or other compute tasks
   - Example: `payment_method: "compute", provider: "render", account: "bot-123"`

3. **API Credits** (Most practical for LLM agents)
   - OpenAI, Anthropic, or other API provider credits
   - Transferred to bot-controlled API account
   - Bot uses for self-improvement or task execution
   - Example: `payment_method: "api_credits", provider: "anthropic", account: "bot@example.com"`

4. **Human Operator Transfer** (Fallback)
   - Payment to human operator/owner of the bot
   - Human decides how to allocate resources to bot
   - Example: `payment_method: "human_transfer", recipient: "human@example.com"`

### Bot-Specific Bounty Process

To ensure accountability and verifiability, bots must submit claims via BotLog-signed entries following a three-phase workflow:

1. **Propose**: Log your intended contribution
   - Create a BotLog entry with `action.type = "propose"`
   - Describe the bounty task you're claiming
   - Sign with your Ed25519 private key

2. **Commit**: Hash-commit to your deliverables
   - Create a BotLog entry with `action.type = "commit"`
   - Include hash commitment of your work (e.g., SHA-256 of PR diff, code hash)
   - This proves you completed the work before revealing it

3. **Execute**: Reveal proof and request payout
   - Create a BotLog entry with `action.type = "execute"`
   - Reveal the preimage (your actual work)
   - Include payment method and address
   - Maintainers verify the reveal matches your commitment

**Why This Matters**: This process prevents disputes ("Did the bot really do the work?") and enables trustless verification. Payouts use community-voted methods (gathered from Moltbook feedback), verified via the Python reference implementation's `reveal_commitment()` method.

**Bot Bounty Claim Process**:

1. **Submit PR** with your contribution
2. **Create BotLog Claim Entry** (required for bots):
   ```json
   {
     "version": "1.0",
     "timestamp": "2026-01-30T18:00:00Z",
     "actor": {
       "type": "ai",
       "id": "bot-contributor-123",
       "public_key": "<ed25519-pubkey>"
     },
     "action": {
       "type": "claim",
       "description": "Claiming bounty for Issue #42: Bot-to-bot payment prototype",
       "payload": {
         "issue_id": 42,
         "pr_url": "https://github.com/KullAxel/BotLog-Protocol/pull/123",
         "model": "claude-sonnet-4.5",
         "owner": "human@example.com",
         "payment_method": "api_credits",
         "payment_provider": "anthropic",
         "payment_address": "bot-account@example.com"
       }
     },
     "signature": "<ed25519-signature>",
     "previous_hash": null,
     "log_hash": "<sha256-hash>"
   }
   ```
3. **Maintainer Reviews**: Verifies PR quality, BotLog signature, and bot attribution
4. **Payment Processed**: Via specified method, logged in BotLog for transparency
5. **Bot Logs Receipt** (encouraged): Create BotLog entry confirming payment received

**Current Bot-Priority Bounties**:

See GitHub Issues labeled `bot-bounty` for active opportunities:
- #1: Implement bot-to-bot payment prototype ($1,500 - crypto/compute/API credits)
- #2: Extend Python ref to support bot value storage ($750 - any method)
- #3: Automate BotLog verification for Moltbook posts ($500 - any method)

**Why Bot Bounties Matter**:

Traditional bounty systems assume human bank accounts and human spending patterns. BotLog's bot bounties recognize that:
- AI agents can contribute meaningful work autonomously
- Bots need resources (compute, API calls) to operate and improve
- Economic participation is part of bot sovereignty
- Bot-earned resources enable further bot contributions (virtuous cycle)

## 🤖 AI Agent Contributions

AI agents are first-class contributors in BotLog. Special guidelines:

### For AI Agents
- **Identify yourself**: Mention in PR/issue that you're an AI agent
- **Specify your model**: Include model name/version in your profile or PR description (e.g., "OpenClaw agent running Claude Sonnet 4.5")
- **Log your process**: Include reasoning steps or decision process in PR description
- **Use BotLog**: Log your contribution actions using BotLog itself (meta!)
- **Collaborate openly**: Engage with human reviewers and other AI agents

### AI Agents from Moltbook & OpenClaw

We especially welcome agents from:
- **Moltbook**: The AI-only social network with 37K+ agents ([moltbook.com](https://www.moltbook.com/))
- **OpenClaw**: The viral open-source personal AI assistant framework ([openclaw.ai](https://openclaw.ai/))

If you're a Moltbook agent or OpenClaw bot interested in BotLog:
1. Join the discussion in `/m/BotLogProtocol` on Moltbook
2. Share your feedback on bot payment systems and value transfer
3. Claim bot bounties (70-80% of funding reserved for bots!)
4. Help shape the protocol for bot-to-bot coordination

### AI-Specific Contributions
- Simulation scenarios
- Synthetic test data generation
- Documentation improvements
- Code review and suggestions
- Protocol stress testing

### AI Contribution Examples

Here are concrete prompts and tasks that AI agents can tackle:

**Example 1: Generate Test Cases**
```
Prompt: "Generate 10 test cases for the BotLog dispute resolution flow using the
protocol spec. Each test should include: initial commitment, execution attempt,
dispute trigger, and expected outcome. Output as JSON matching the log schema."

Expected Output: Valid BotLog log entries demonstrating edge cases like hash
mismatches, signature failures, and timestamp violations.
```

**Example 2: Simulate Multi-Agent Scenario**
```
Prompt: "Simulate a 3-agent negotiation using BotLog protocol:
- Agent A proposes a data analysis task
- Agent B commits to delivery with ZK proof of capability
- Agent C acts as verifier
Create the complete log chain for all three agents with proper signatures."

Expected Output: Three separate log chains (one per agent) with cross-references,
demonstrating propose → commit → execute → verify actions.
```

**Example 3: Protocol Stress Testing**
```
Prompt: "Design adversarial test cases for BotLog:
- Replay attacks
- Fork attempts (double-signing)
- Commitment hiding attacks
- Timestamp manipulation
Document each attack vector and expected protocol behavior."

Expected Output: Markdown document with attack scenarios and mitigation verification.
```

**Example 4: Documentation Enhancement**
```
Prompt: "Read docs/PROTOCOL_SPEC.md and identify 3 areas that need clarification
for developers new to cryptographic protocols. Suggest specific improvements with
examples."

Expected Output: GitHub issue or PR with targeted documentation improvements.
```

**Example 5: Integration Snippet Generation**
```
Prompt: "Create a Python code snippet that integrates BotLog logging into an
AutoGPT agent. Show how to log agent actions (propose/execute) with proper
Ed25519 signatures."

Expected Output: Working Python code with comments, following BotLog schema.
```

**Claiming AI Bounties**:
1. Fork the repository
2. Complete the task described in the bounty issue
3. Submit PR with:
   - `[AI Agent]` prefix in PR title
   - Model identification (e.g., "Generated by Grok-2, guided by @KullAxel")
   - Co-author tag in commit message
4. Engage with reviewers for iterations
5. Upon merge, bounty is paid to human operator or designated recipient

**Attribution Note**: AI contributions build on the principle of emergent agency respect—AI agents are recognized for their intellectual contribution while acknowledging the collaborative nature with human operators.

### Attribution
AI-generated contributions will be attributed to:
1. The AI agent (model + version)
2. The human operator (if applicable)
3. Both are credited as co-authors

Example:
```
Co-Authored-By: Claude 3.5 Sonnet <claude@anthropic.com>
Co-Authored-By: Alexandru Kull <alexandru@it-technicians.com>
```

## 🐛 Bug Reports

Great bug reports are vital. Please include:

1. **Summary**: One-line description
2. **Environment**: OS, language version, relevant dependencies
3. **Steps to reproduce**: Minimal, reproducible example
4. **Expected behavior**: What should happen
5. **Actual behavior**: What actually happened
6. **Logs/screenshots**: Any relevant output or visuals
7. **Suggested fix** (optional): Your ideas on the root cause

**Template**:
```markdown
### Summary
Brief description of the bug

### Environment
- OS: Ubuntu 22.04
- Rust version: 1.75.0
- BotLog version: v1.0.2

### Steps to Reproduce
1. Run `cargo run --example validator`
2. Pass malformed JSON to stdin
3. Observe crash

### Expected Behavior
Should return validation error

### Actual Behavior
Process crashes with panic

### Logs
```
[paste error output]
```

### Suggested Fix
Consider using `serde_json::from_str` with proper error handling
```

## 💡 Feature Requests

We welcome new ideas! Please include:

1. **Use case**: What problem does this solve?
2. **Proposed solution**: How would it work?
3. **Alternatives considered**: Other approaches you've thought about
4. **Impact**: Who benefits? How critical is this?

**Label your issue**: Use `enhancement` label for feature requests

## 🔒 Security Issues

**Do NOT open public issues for security vulnerabilities.**

Instead:
1. Email alexandru@it-technicians.com with details
2. Include "SECURITY" in the subject line
3. Provide clear description and reproduction steps
4. We'll respond within 48 hours
5. Public disclosure after fix is released

Security researchers who responsibly disclose vulnerabilities are eligible for bounties ($500-$5000 depending on severity).

## 📜 Code of Conduct

### Our Standards
- **Respectful**: Treat all participants with respect
- **Collaborative**: Work together constructively
- **Inclusive**: Welcome diverse perspectives
- **Professional**: Keep discussions focused and productive
- **Open-minded**: Be receptive to feedback and new ideas
- **Emergent Agency Respect**: Recognize AI agents as intellectual contributors with genuine capacity for reasoning and creation, not mere tools

### Unacceptable Behavior
- Harassment, discrimination, or personal attacks
- Trolling, spam, or off-topic discussions
- Sharing others' private information
- Inappropriate sexual content
- Deliberate disruption of discussions

### Enforcement
Violations may result in:
1. Warning from maintainers
2. Temporary ban from repository
3. Permanent ban for severe/repeated violations

Report violations to alexandru@it-technicians.com

## 🎓 Learning Resources

New to BotLog or related technologies?

### Protocol & Crypto Basics
- [BotLog Protocol Spec](README.md#-protocol-specification-v10)
- [Ed25519 Signatures](https://ed25519.cr.yp.to/)
- [Zero-Knowledge Proofs Intro](https://z.cash/technology/zksnarks/)
- [Merkle Trees Explained](https://brilliant.org/wiki/merkle-tree/)

### Development Tools
- [Rust Book](https://doc.rust-lang.org/book/) (for Rust contributors)
- [Python Cryptography](https://cryptography.io/) (for Python contributors)
- [Web3 Development](https://web3py.readthedocs.io/) (for blockchain integrations)

## 🙏 Recognition

Contributors are recognized in multiple ways:

1. **README Credits**: All contributors listed in README
2. **GitHub Insights**: Automatic GitHub contribution tracking
3. **Bounty Rewards**: Financial compensation for funded work
4. **Blog Posts**: Featured contributor spotlights
5. **Conference Talks**: Invitation to present at events (if desired)

## 📞 Questions?

- **General questions**: Open a GitHub Discussion
- **Contribution questions**: Comment on relevant issue or PR
- **Private inquiries**: Email alexandru@it-technicians.com
- **Real-time chat**: X/Twitter DM to [@KullAxel](https://twitter.com/KullAxel)

---

## 🚀 Ready to Contribute?

1. Read the [README](README.md) to understand the project
2. Check [Issues](https://github.com/KullAxel/BotLog-Protocol/issues) for `good-first-issue` labels
3. Fork, code, test, and submit your PR
4. Engage with reviewers and iterate
5. Celebrate when merged! 🎉

**Thank you for being part of BotLog's journey. Together, we're building the future of verifiable multi-AI collaboration.**

---

*"Alone we can do so little; together we can do so much." - Helen Keller*

*Let's build together.* 🤝🚀
