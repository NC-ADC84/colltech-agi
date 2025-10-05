import time
import sys
import os

# Ensure repository packages (sibling folders) are importable when tests run from colltech-agi
THIS_DIR = os.path.abspath(os.path.dirname(__file__))
COLLTECH_ROOT = os.path.abspath(os.path.join(THIS_DIR, '..'))
# The workspace root is the parent of colltech-agi in this workspace layout
WORKSPACE_ROOT = os.path.abspath(os.path.join(COLLTECH_ROOT, '..'))

for p in (COLLTECH_ROOT, WORKSPACE_ROOT):
    if p not in sys.path:
        sys.path.insert(0, p)

# Also ensure explicit sibling package folders are present
POSSIBLE_PKGS = [
    os.path.abspath(os.path.join(WORKSPACE_ROOT, 'Bots')),
    os.path.abspath(os.path.join(WORKSPACE_ROOT, 'RAS')),
]
for p in POSSIBLE_PKGS:
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)

from RAS.ras_core import BridgePrimitives
from Bots.bridge_system import CollTechBridge, BridgeMessage, Platform, MessageType
from Bots.language_packs import SEEDSLanguagePack


def test_bridgeprimitives_rx_accepts_valid_signed_env_and_rejects_invalid():
    # Build a simple envelope
    env = {"foo": "bar", "n": 1}

    # Produce a signed envelope using tx()
    signed = BridgePrimitives.tx(env)

    # rx should accept the freshly signed envelope and return the original envelope
    out = BridgePrimitives.rx(signed)
    assert out == env

    # If the signature is tampered with, rx should reject
    bad = dict(signed)
    bad["signature"] = "bad-signature"
    assert BridgePrimitives.rx(bad) is None

    # If the timestamp is a numeric-like string, rx should accept it
    signed_str_ts = dict(signed)
    signed_str_ts["timestamp"] = str(signed_str_ts["timestamp"])
    assert BridgePrimitives.rx(signed_str_ts) == env

    # If the timestamp is outside the 10-minute window, rx should reject
    old = dict(signed)
    old["timestamp"] = time.time() - 700  # older than 600s
    assert BridgePrimitives.rx(old) is None


def test_colltechbridge_replay_detection_records_and_detects_replay():
    bridge = CollTechBridge()

    # Create a bridge message
    msg = bridge.create_bridge_message(
        content="hello",
        source_platform=Platform.DISCORD,
        target_platform=Platform.REDDIT,
        message_type=MessageType.USER_MESSAGE
    )

    # First check: not a replay
    assert bridge._is_replay_attack(msg) is False

    # Second check: should now be detected as a replay
    assert bridge._is_replay_attack(msg) is True


def test_seeds_echoform_activation_for_signal_inputs():
    seeds = SEEDSLanguagePack()

    # Provide an input containing echoform signals
    result = seeds.process_input("c01 pisces seed")

    # Activation should produce ECHOFORM state and echoform_active True
    assert isinstance(result, dict)
    assert result.get("state") in ("ECHOFORM", "INITIATION_ECHO") or result.get("echoform_active") is True
    # Prefer explicit echo activation
    if result.get("state") == "ECHOFORM":
        assert result.get("echoform_active") is True
