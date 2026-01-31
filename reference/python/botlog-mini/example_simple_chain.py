#!/usr/bin/env python3
"""
BotLog Protocol - Simple Chain Example

This example demonstrates:
1. Generating an Ed25519 keypair
2. Creating a chain of linked log entries
3. Verifying signatures and chain integrity
4. Basic propose -> commit -> execute workflow
"""

import json
from botlog import (
    BotLogEntry,
    generate_keypair,
    public_key_to_base64,
    verify_chain,
    get_current_timestamp
)


def main():
    print("=" * 70)
    print("BotLog Protocol - Simple Chain Example")
    print("=" * 70)
    print()

    # Step 1: Generate keypair for the actor
    print("📌 Step 1: Generating Ed25519 keypair...")
    private_key, public_key = generate_keypair()
    public_key_b64 = public_key_to_base64(public_key)
    print(f"   ✓ Public key: {public_key_b64[:24]}...")
    print()

    # Actor info
    actor_info = {
        "type": "human",
        "id": "KullAxel",
        "public_key": public_key_b64
    }

    # Step 2: Create genesis entry (propose)
    print("📌 Step 2: Creating genesis entry (propose)...")
    entry1 = BotLogEntry(
        timestamp=get_current_timestamp(),
        actor=actor_info,
        action={
            "type": "propose",
            "description": "Launch BotLog feedback campaign",
            "payload": {
                "task": "Gather feedback from AI agent community",
                "platforms": ["Moltbook", "X"],
                "timeline": "7 days"
            }
        },
        previous_hash=None  # Genesis entry
    )
    entry1.sign(private_key)
    print(f"   ✓ Entry 1 created and signed")
    print(f"   ✓ Log hash: {entry1.log_hash[:32]}...")
    print()

    # Step 3: Create second entry (commit)
    print("📌 Step 3: Creating second entry (commit)...")
    entry2 = BotLogEntry(
        timestamp=get_current_timestamp(),
        actor=actor_info,
        action={
            "type": "commit",
            "description": "Commit to delivering feedback summary",
            "payload": {
                "deliverable": "feedback_summary.md",
                "deadline": "2026-02-07T00:00:00Z"
            }
        },
        previous_hash=entry1.log_hash  # Link to previous entry
    )
    entry2.sign(private_key)
    print(f"   ✓ Entry 2 created and signed")
    print(f"   ✓ Previous hash: {entry2.previous_hash[:32]}...")
    print(f"   ✓ Log hash: {entry2.log_hash[:32]}...")
    print()

    # Step 4: Create third entry (execute)
    print("📌 Step 4: Creating third entry (execute)...")
    entry3 = BotLogEntry(
        timestamp=get_current_timestamp(),
        actor=actor_info,
        action={
            "type": "execute",
            "description": "Delivered feedback summary",
            "payload": {
                "deliverable_url": "https://github.com/KullAxel/BotLog-Protocol/feedback_summary.md",
                "summary": "Received 15 suggestions from bot community"
            }
        },
        previous_hash=entry2.log_hash  # Link to previous entry
    )
    entry3.sign(private_key)
    print(f"   ✓ Entry 3 created and signed")
    print(f"   ✓ Previous hash: {entry3.previous_hash[:32]}...")
    print(f"   ✓ Log hash: {entry3.log_hash[:32]}...")
    print()

    # Step 5: Verify the complete chain
    print("📌 Step 5: Verifying chain integrity...")
    chain = [entry1, entry2, entry3]

    if verify_chain(chain):
        print("   ✅ Chain verification PASSED!")
        print("   - All signatures are valid")
        print("   - All hashes are correct")
        print("   - Chain linkage is intact")
        print("   - Timestamps are properly ordered")
    else:
        print("   ❌ Chain verification FAILED!")
        return

    print()

    # Step 6: Display the chain
    print("📌 Step 6: Complete chain (JSON):")
    print()
    for i, entry in enumerate(chain, 1):
        print(f"--- Entry {i} ({entry.action['type']}) ---")
        print(json.dumps(entry.to_dict(include_log_hash=True), indent=2))
        print()

    # Step 7: Test chain integrity by tampering
    print("📌 Step 7: Testing tamper detection...")
    print("   Attempting to modify entry 2's action description...")

    # Create a copy and tamper with it
    tampered_entry2 = BotLogEntry.from_dict(entry2.to_dict(include_log_hash=True))
    tampered_entry2.action["description"] = "TAMPERED: Different description"

    # Try to verify the tampered chain
    tampered_chain = [entry1, tampered_entry2, entry3]
    print()
    if verify_chain(tampered_chain):
        print("   ❌ Tamper detection FAILED! (This shouldn't happen)")
    else:
        print("   ✅ Tamper detection PASSED! (Chain correctly rejected)")

    print()
    print("=" * 70)
    print("Demo complete! 🎉")
    print("=" * 70)


if __name__ == "__main__":
    main()
