# BotLog Protocol - Integration Examples

**Status**: Draft
**Last Updated**: 2026-01-31

This document provides concrete integration examples for popular AI agent frameworks, demonstrating how to add BotLog verifiable logging to existing systems.

---

## Table of Contents

1. [Bittensor Integration](#bittensor-integration)
2. [AutoGPT Integration](#autogpt-integration)
3. [LangChain Integration](#langchain-integration)
4. [Custom Agent Integration](#custom-agent-integration)

---

## Bittensor Integration

### Overview

Integrate BotLog logging into Bittensor validators and miners to create verifiable action trails for subnet operations.

### Example: Miner with BotLog Logging

```python
import bittensor as bt
import hashlib
import json
from nacl.signing import SigningKey
from datetime import datetime

class BotLogMiner(bt.Miner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize BotLog identity
        self.signing_key = SigningKey.generate()
        self.public_key = self.signing_key.verify_key
        self.log_chain = []

    def _create_log_entry(self, action_type, description, payload):
        """Create a BotLog-compliant log entry"""
        # Build entry without signature first
        entry = {
            "version": "1.0",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "actor": {
                "type": "ai",
                "id": f"bittensor-miner-{self.wallet.hotkey.ss58_address}",
                "public_key": self.public_key.encode().hex()
            },
            "action": {
                "type": action_type,
                "description": description,
                "payload": payload
            },
            "commitments": [],
            "previous_hash": self.log_chain[-1]["log_hash"] if self.log_chain else None,
            "signature": "",
            "log_hash": ""
        }

        # Sign the entry
        canonical = json.dumps(entry, sort_keys=True, separators=(',', ':'))
        signature = self.signing_key.sign(canonical.encode())
        entry["signature"] = signature.signature.hex()

        # Compute log hash
        entry["log_hash"] = hashlib.sha256(
            json.dumps(entry, sort_keys=True).encode()
        ).hexdigest()

        self.log_chain.append(entry)
        return entry

    def forward(self, synapse):
        # Log the proposal
        self._create_log_entry(
            "propose",
            f"Received forward request from validator",
            {
                "synapse_type": synapse.__class__.__name__,
                "dendrite_hotkey": synapse.dendrite.hotkey
            }
        )

        # Process the request
        response = self.process_request(synapse)

        # Log the execution
        self._create_log_entry(
            "execute",
            f"Completed forward processing",
            {
                "success": True,
                "response_size": len(str(response))
            }
        )

        return response

    def publish_logs(self, storage_backend="ipfs"):
        """Publish log chain to decentralized storage"""
        log_data = json.dumps(self.log_chain, indent=2)
        # Upload to IPFS/Arweave/etc.
        # Return CID/hash for verification
        pass
```

### Use Cases

- **Validator Accountability**: Validators log scoring decisions with commitments
- **Miner Provenance**: Miners prove work completion with verifiable logs
- **Subnet Governance**: Log protocol upgrade proposals and votes
- **Incentive Transparency**: Verifiable records of emission distributions

---

## AutoGPT Integration

### Overview

Add BotLog logging to AutoGPT agents to create audit trails of autonomous actions.

### Example: AutoGPT Plugin

```python
from autogpt.agent import Agent
from autogpt.commands.command import command
import hashlib
import json
from nacl.signing import SigningKey
from datetime import datetime

class BotLogPlugin:
    """AutoGPT plugin for BotLog protocol logging"""

    def __init__(self):
        self.signing_key = SigningKey.generate()
        self.public_key = self.signing_key.verify_key
        self.log_chain = []

    def can_handle_post_planning(self) -> bool:
        return True

    def can_handle_post_command(self) -> bool:
        return True

    def post_planning(self, plan: str) -> str:
        """Log agent's plan as a proposal"""
        self._log_action(
            "propose",
            "Agent created execution plan",
            {"plan": plan}
        )
        return plan

    def post_command(self, command_name: str, arguments: dict, result: str):
        """Log command execution"""
        self._log_action(
            "execute",
            f"Executed command: {command_name}",
            {
                "command": command_name,
                "arguments": arguments,
                "result_preview": result[:200] if result else None
            }
        )

    def _log_action(self, action_type, description, payload):
        entry = {
            "version": "1.0",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "actor": {
                "type": "ai",
                "id": f"autogpt-agent-{self.public_key.encode().hex()[:16]}",
                "public_key": self.public_key.encode().hex()
            },
            "action": {
                "type": action_type,
                "description": description,
                "payload": payload
            },
            "commitments": [],
            "previous_hash": self.log_chain[-1]["log_hash"] if self.log_chain else None,
            "signature": "",
            "log_hash": ""
        }

        canonical = json.dumps(entry, sort_keys=True, separators=(',', ':'))
        signature = self.signing_key.sign(canonical.encode())
        entry["signature"] = signature.signature.hex()
        entry["log_hash"] = hashlib.sha256(
            json.dumps(entry, sort_keys=True).encode()
        ).hexdigest()

        self.log_chain.append(entry)

        # Optionally: publish to storage backend
        self._publish_entry(entry)

    def _publish_entry(self, entry):
        """Publish log entry to decentralized storage or local file"""
        with open("autogpt_botlog.jsonl", "a") as f:
            f.write(json.dumps(entry) + "\n")

# Usage in AutoGPT config
PLUGINS = ["BotLogPlugin"]
```

### Use Cases

- **Autonomous Action Trails**: Track all commands executed by AutoGPT
- **Plan Verification**: Verify agent followed proposed plan
- **Multi-Agent Coordination**: Multiple AutoGPT instances coordinate via BotLog
- **Human Oversight**: Humans review and verify agent actions

---

## LangChain Integration

### Overview

Add BotLog logging to LangChain agents and chains for verifiable LLM workflows.

### Example: LangChain Callback Handler

```python
from langchain.callbacks.base import BaseCallbackHandler
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.chat_models import ChatOpenAI
import hashlib
import json
from nacl.signing import SigningKey
from datetime import datetime

class BotLogCallbackHandler(BaseCallbackHandler):
    """LangChain callback handler for BotLog protocol"""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.signing_key = SigningKey.generate()
        self.public_key = self.signing_key.verify_key
        self.log_chain = []

    def on_agent_action(self, action, **kwargs):
        """Log agent actions"""
        self._log_entry(
            "propose",
            f"Agent planning to use tool: {action.tool}",
            {
                "tool": action.tool,
                "tool_input": str(action.tool_input),
                "log": action.log
            }
        )

    def on_tool_end(self, output, **kwargs):
        """Log tool execution results"""
        self._log_entry(
            "execute",
            "Tool execution completed",
            {
                "output": str(output)[:500]  # Truncate long outputs
            }
        )

    def on_chain_end(self, outputs, **kwargs):
        """Log chain completion"""
        self._log_entry(
            "execute",
            "Chain execution completed",
            {
                "outputs": str(outputs)[:500]
            }
        )

    def _log_entry(self, action_type, description, payload):
        entry = {
            "version": "1.0",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "actor": {
                "type": "ai",
                "id": self.agent_id,
                "public_key": self.public_key.encode().hex()
            },
            "action": {
                "type": action_type,
                "description": description,
                "payload": payload
            },
            "commitments": [],
            "previous_hash": self.log_chain[-1]["log_hash"] if self.log_chain else None,
            "signature": "",
            "log_hash": ""
        }

        canonical = json.dumps(entry, sort_keys=True, separators=(',', ':'))
        signature = self.signing_key.sign(canonical.encode())
        entry["signature"] = signature.signature.hex()
        entry["log_hash"] = hashlib.sha256(
            json.dumps(entry, sort_keys=True).encode()
        ).hexdigest()

        self.log_chain.append(entry)

    def export_logs(self, filepath="langchain_botlog.json"):
        """Export complete log chain"""
        with open(filepath, "w") as f:
            json.dump(self.log_chain, f, indent=2)

# Usage
llm = ChatOpenAI(model="gpt-4")
botlog_handler = BotLogCallbackHandler(agent_id="langchain-agent-001")

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    callbacks=[botlog_handler],
    verbose=True
)

result = agent_executor.run("Analyze customer sentiment from reviews")
botlog_handler.export_logs()
```

### Use Cases

- **LLM Chain Auditing**: Verify multi-step reasoning chains
- **RAG Provenance**: Track retrieval and generation steps
- **Agent Tool Usage**: Log which tools were invoked and why
- **Prompt Injection Detection**: Verify expected vs actual tool usage

---

## Custom Agent Integration

### Minimal Integration Template

```python
import hashlib
import json
from nacl.signing import SigningKey, VerifyKey
from datetime import datetime

class BotLogAgent:
    """Minimal BotLog-enabled agent"""

    def __init__(self, agent_id: str, agent_type: str = "ai"):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.signing_key = SigningKey.generate()
        self.public_key = self.signing_key.verify_key
        self.log_chain = []

    def log_action(self, action_type, description, payload=None, commitments=None):
        """Log an action to the BotLog chain"""
        entry = {
            "version": "1.0",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "actor": {
                "type": self.agent_type,
                "id": self.agent_id,
                "public_key": self.public_key.encode().hex()
            },
            "action": {
                "type": action_type,
                "description": description,
                "payload": payload or {}
            },
            "commitments": commitments or [],
            "previous_hash": self.log_chain[-1]["log_hash"] if self.log_chain else None,
            "signature": "",
            "log_hash": ""
        }

        # Sign
        canonical = json.dumps(entry, sort_keys=True, separators=(',', ':'))
        signature = self.signing_key.sign(canonical.encode())
        entry["signature"] = signature.signature.hex()

        # Hash
        entry["log_hash"] = hashlib.sha256(
            json.dumps(entry, sort_keys=True).encode()
        ).hexdigest()

        self.log_chain.append(entry)
        return entry

    def verify_chain(self):
        """Verify integrity of the log chain"""
        for i, entry in enumerate(self.log_chain):
            # Verify hash chain
            if i > 0:
                expected_prev = self.log_chain[i-1]["log_hash"]
                if entry["previous_hash"] != expected_prev:
                    return False, f"Hash chain broken at entry {i}"

            # Verify signature
            entry_copy = entry.copy()
            signature_bytes = bytes.fromhex(entry_copy.pop("signature"))
            entry_copy["signature"] = ""
            canonical = json.dumps(entry_copy, sort_keys=True, separators=(',', ':'))

            try:
                verify_key = VerifyKey(bytes.fromhex(entry["actor"]["public_key"]))
                verify_key.verify(canonical.encode(), signature_bytes)
            except Exception as e:
                return False, f"Signature verification failed at entry {i}: {e}"

        return True, "Chain verified successfully"

# Usage Example
agent = BotLogAgent("my-custom-agent-001")

# Log a proposal
agent.log_action(
    "propose",
    "Proposing to analyze dataset",
    {"dataset": "customer_reviews.csv", "method": "sentiment_analysis"}
)

# Log execution
agent.log_action(
    "execute",
    "Completed sentiment analysis",
    {"positive": 45, "neutral": 30, "negative": 25}
)

# Verify chain integrity
valid, message = agent.verify_chain()
print(f"Chain valid: {valid} - {message}")
```

---

## Best Practices

1. **Initialize Early**: Create BotLog identity at agent startup
2. **Log Atomically**: Each significant action should have one log entry
3. **Use Commitments**: For multi-step processes, commit first, then reveal
4. **Publish Regularly**: Push logs to decentralized storage periodically
5. **Verify on Load**: Always verify chain integrity when loading existing logs
6. **Handle Disputes**: Implement dispute resolution for multi-agent scenarios
7. **Respect Privacy**: Use ZK proofs or encrypted payloads for sensitive data

---

## Storage Backend Options

- **Local File**: Simple append-only JSONL file
- **IPFS**: Decentralized, content-addressed storage
- **Arweave**: Permanent storage with one-time payment
- **Database**: PostgreSQL/MongoDB with append-only constraints
- **Blockchain**: Ethereum/Polygon for high-value coordination

---

## Next Steps

- Implement these examples for your use case
- Submit integration guides as PRs to this doc
- Claim bounties for production-ready integrations
- Share your integration on X with #BotLogProtocol

---

**Questions?** Open an issue or discussion on GitHub!
