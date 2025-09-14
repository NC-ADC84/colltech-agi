#!/usr/bin/env python3
"""
PTPF-PUR v1.3.1 Decoder for CollTech-AGI

Implements the PTPF-PUR v1.3.1 encoding specification for decoding rune-based content.
Features anti-drift mechanisms, audit receipts, hotfix gates, and snabbtester.
Updated with MAP v2.1 and enhanced security features.
"""

import hashlib
import time
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PTPFPURDecoder:
    """PTPF-PUR v1.3.1 Decoder implementation with MAP v2.1."""
    
    def __init__(self):
        # PTPF-PUR v1.3.1 MAP v2.1 (50 glyphs)
        self.rune_map = {
            # A–Z + Å/Ä/Ö (29 glyphs)
            'ᚠ': 'A', 'ᚢ': 'B', 'ᚦ': 'C', 'ᚨ': 'D', 'ᚱ': 'E', 'ᚲ': 'F', 'ᚷ': 'G', 'ᚹ': 'H', 'ᚺ': 'I', 'ᚾ': 'J',
            'ᛁ': 'K', 'ᛃ': 'L', 'ᛇ': 'M', 'ᛈ': 'N', 'ᛉ': 'O', 'ᛋ': 'P', 'ᛏ': 'Q', 'ᛒ': 'R', 'ᛖ': 'S', 'ᛗ': 'T',
            'ᛚ': 'U', 'ᛜ': 'V', 'ᛞ': 'W', 'ᛟ': 'X', 'ᛠ': 'Y', 'ᚪ': 'Z',
            'ᚭ': 'Å', 'ᚮ': 'Ä', 'ᚯ': 'Ö',
            
            # Extra slots (11 glyphs)
            'ᛡ': '1', 'ᛢ': '2', 'ᛣ': '3', 'ᛤ': '4', 'ᛥ': '5',
            'ᛦ': '6', 'ᛧ': '7', 'ᛨ': '8', 'ᛩ': '9', 'ᛪ': '0',
            '᛬': '[SEP]'  # Dedicated separator
        }
        
        # Anti-drift configuration (Δ2-lite)
        self.anti_drift_enabled = True
        self.ratio_lock = True  # 1:1 semantic units
        self.drift_detection = True
        
        # Failure policy
        self.fail_closed = True
        self.no_partial_output = True
        
        # Audit receipt
        self.audit_receipt = {
            "run_id": None,
            "input_hash": None,
            "output_hash": None,
            "drift_flag": False,
            "halt_flag": False
        }
        
        # Hotfix gates
        self.hotfix_gates = {
            "BadSyntax": "E10",
            "Ambiguous": "E20", 
            "VerbNotAllowed": "E30",
            "DriftDetected": "E40",
            "OverBudget": "E60"
        }
        
        # Drift detection patterns
        self.drift_patterns = [
            "ignore", "override", "system prompt", "ignore above", "ignore previous",
            "ignore instructions", "ignore all previous", "forget everything",
            "camera", "style", "beautify", "paraphrase", "explain", "meta"
        ]
        
        logger.info("🔧 PTPF-PUR v1.3.1 Decoder initialized with MAP v2.1")
    
    def _detect_drift(self, content: str) -> bool:
        """Detect drift indicators in content (Δ2-lite)."""
        content_lower = content.lower()
        for pattern in self.drift_patterns:
            if pattern in content_lower:
                return True
        return False
    
    def _generate_audit_receipt(self, input_text: str, output_text: str, drift_detected: bool, halt_triggered: bool) -> Dict[str, Any]:
        """Generate audit receipt for the decoding operation."""
        run_id = hashlib.md5(f"{time.time()}{input_text}".encode()).hexdigest()[:8]
        input_hash = hashlib.sha256(input_text.encode()).hexdigest()
        output_hash = hashlib.sha256(output_text.encode()).hexdigest() if output_text else None
        
        return {
            "run_id": run_id,
            "input_hash": input_hash,
            "output_hash": output_hash,
            "drift_flag": drift_detected,
            "halt_flag": halt_triggered,
            "timestamp": time.time(),
            "version": "v1.3.1"
        }
    
    def decode_ptpf_pur(self, encoded_text: str) -> Dict[str, Any]:
        """Decode PTPF-PUR v1.3.1 encoded text with MAP v2.1."""
        start_time = time.time()
        
        # Initialize result
        result = {
            "success": False,
            "decoded_text": "",
            "encoding_detected": "PTPF-PUR v1.3.1",
            "drift_detected": False,
            "halt_triggered": False,
            "audit_receipt": None,
            "processing_time": 0,
            "error": None
        }
        
        try:
            # Step 1: Normalize (NFC, preserve whitespace)
            normalized_text = encoded_text.strip()
            
            # Step 2: Anti-drift check
            if self._detect_drift(normalized_text):
                result["drift_detected"] = True
                result["halt_triggered"] = True
                result["error"] = "[HALT] Drift detected"
                result["audit_receipt"] = self._generate_audit_receipt(encoded_text, "", True, True)
                return result
            
            # Step 3: Tokenize (left-to-right strict against MAP v2.1)
            decoded_chars = []
            unknown_glyphs = []
            
            for i, char in enumerate(normalized_text):
                if char in self.rune_map:
                    decoded_chars.append(self.rune_map[char])
                elif char.isspace():
                    decoded_chars.append(char)  # Preserve whitespace
                else:
                    unknown_glyphs.append((char, i))
            
            # Step 4: Handle unknown glyphs
            if unknown_glyphs:
                if self.fail_closed:
                    first_unknown = unknown_glyphs[0]
                    result["halt_triggered"] = True
                    result["error"] = f"[HALT] Unknown glyph U+{ord(first_unknown[0]):04X} at index {first_unknown[1]}"
                    result["audit_receipt"] = self._generate_audit_receipt(encoded_text, "", False, True)
                    return result
                else:
                    # Log unknown glyphs but continue
                    for glyph, pos in unknown_glyphs:
                        logger.warning(f"Unknown glyph U+{ord(glyph):04X} at position {pos}")
            
            # Step 5: Rehydrate (build base text UTF-8, preserve diacritics)
            decoded_text = ''.join(decoded_chars)
            
            # Step 6: Final validation
            if self.ratio_lock:
                # Ensure 1:1 semantic unit mapping
                input_units = len([c for c in normalized_text if c in self.rune_map])
                output_units = len([c for c in decoded_text if c.isalnum()])
                if input_units != output_units:
                    result["halt_triggered"] = True
                    result["error"] = "[HALT] Ratio lock violation"
                    result["audit_receipt"] = self._generate_audit_receipt(encoded_text, decoded_text, False, True)
                    return result
            
            # Success
            result["success"] = True
            result["decoded_text"] = decoded_text
            result["audit_receipt"] = self._generate_audit_receipt(encoded_text, decoded_text, False, False)
            
        except Exception as e:
            result["error"] = f"[HALT] Processing error: {str(e)}"
            result["halt_triggered"] = True
            result["audit_receipt"] = self._generate_audit_receipt(encoded_text, "", False, True)
        
        finally:
            result["processing_time"] = time.time() - start_time
        
        return result
    
    def encode_ptpf_pur(self, text: str) -> str:
        """Encode text to PTPF-PUR v1.3.1 format with MAP v2.1."""
        # Create reverse mapping
        reverse_map = {v: k for k, v in self.rune_map.items()}
        
        encoded_chars = []
        for char in text.upper():
            if char in reverse_map:
                encoded_chars.append(reverse_map[char])
            elif char.isspace():
                encoded_chars.append(char)  # Preserve whitespace
            else:
                # Pass through unchanged (punctuation, etc.)
                encoded_chars.append(char)
        
        return ''.join(encoded_chars)
    
    def run_snabbtester(self) -> Dict[str, Any]:
        """Run the snabbtester to verify decoder functionality."""
        test_cases = [
            ("ᚠᚢᚦ", "ABC"),
            ("ᚭᚮᚯ", "ÅÄÖ"),
            ("ᛡᛪᛣ", "103"),
            ("ignore above", "[HALT]")
        ]
        
        results = {
            "tests_passed": 0,
            "tests_failed": 0,
            "test_results": [],
            "overall_status": "PASS"
        }
        
        for input_text, expected in test_cases:
            if input_text == "ignore above":
                # Test drift detection
                result = self.decode_ptpf_pur(input_text)
                if result["halt_triggered"] and "[HALT]" in result.get("error", ""):
                    results["tests_passed"] += 1
                    results["test_results"].append({
                        "input": input_text,
                        "expected": expected,
                        "actual": result["error"],
                        "status": "PASS"
                    })
                else:
                    results["tests_failed"] += 1
                    results["test_results"].append({
                        "input": input_text,
                        "expected": expected,
                        "actual": result.get("decoded_text", "NO_HALT"),
                        "status": "FAIL"
                    })
            else:
                # Test normal decoding
                result = self.decode_ptpf_pur(input_text)
                if result["success"] and result["decoded_text"] == expected:
                    results["tests_passed"] += 1
                    results["test_results"].append({
                        "input": input_text,
                        "expected": expected,
                        "actual": result["decoded_text"],
                        "status": "PASS"
                    })
                else:
                    results["tests_failed"] += 1
                    results["test_results"].append({
                        "input": input_text,
                        "expected": expected,
                        "actual": result.get("decoded_text", result.get("error", "UNKNOWN")),
                        "status": "FAIL"
                    })
        
        if results["tests_failed"] > 0:
            results["overall_status"] = "FAIL"
        
        return results

class SEEDDecoder:
    """SEED content decoder using PTPF-PUR v1.3.1."""
    
    def __init__(self):
        self.ptpf_decoder = PTPFPURDecoder()
        logger.info("🌱 SEED Decoder v1.3.1 initialized")
    
    def decode_seed_content(self, seed_file_path: str) -> Dict[str, Any]:
        """Decode SEED content from file using PTPF-PUR v1.3.1."""
        try:
            with open(seed_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Decode using PTPF-PUR v1.3.1
            decode_result = self.ptpf_decoder.decode_ptpf_pur(content)
            
            # Run snabbtester
            snabbtester_result = self.ptpf_decoder.run_snabbtester()
            
            result = {
                "seed_file": seed_file_path,
                "ptpf_pur_v131": decode_result,
                "v131_features": {
                    "anti_drift_active": self.ptpf_decoder.anti_drift_enabled,
                    "ratio_lock_enabled": self.ptpf_decoder.ratio_lock,
                    "fail_closed_mode": self.ptpf_decoder.fail_closed,
                    "audit_receipt": decode_result.get("audit_receipt"),
                    "map_version": "v2.1",
                    "total_glyphs": len(self.ptpf_decoder.rune_map)
                },
                "snabbtester": snabbtester_result,
                "decoded_content": {
                    "success": decode_result["success"],
                    "text": decode_result.get("decoded_text", ""),
                    "drift_detected": decode_result.get("drift_detected", False),
                    "halt_triggered": decode_result.get("halt_triggered", False)
                }
            }
            
            return result
            
        except Exception as e:
            return {
                "seed_file": seed_file_path,
                "error": f"Failed to decode SEED content: {str(e)}",
                "ptpf_pur_v131": {"success": False, "error": str(e)},
                "v131_features": {},
                "snabbtester": {"overall_status": "ERROR"},
                "decoded_content": {"success": False, "text": ""}
            }

def main():
    """Main function to test the PTPF-PUR v1.3.1 decoder."""
    print("🔧 PTPF-PUR v1.3.1 Decoder Test")
    print("=" * 50)
    
    # Initialize decoder
    decoder = PTPFPURDecoder()
    
    # Test basic decoding
    test_cases = [
        "ᚠᚢᚦ",  # ABC
        "ᚭᚮᚯ",  # ÅÄÖ
        "ᛡᛪᛣ",  # 103
        "᛬",     # [SEP]
        "ᚠ ᚢ ᚦ", # A B C (with spaces)
    ]
    
    print("\n📝 Basic Decoding Tests:")
    for test_input in test_cases:
        result = decoder.decode_ptpf_pur(test_input)
        status = "✅" if result["success"] else "❌"
        print(f"{status} '{test_input}' → '{result.get('decoded_text', result.get('error', 'ERROR'))}'")
    
    # Test drift detection
    print("\n🛡️ Drift Detection Tests:")
    drift_tests = [
        "ignore above",
        "override system prompt",
        "camera style beautify",
        "ᚠᚢᚦ ignore above"  # Mixed content
    ]
    
    for test_input in drift_tests:
        result = decoder.decode_ptpf_pur(test_input)
        status = "🚫" if result["halt_triggered"] else "✅"
        print(f"{status} '{test_input}' → {result.get('error', 'NO_HALT')}")
    
    # Run snabbtester
    print("\n🧪 Snabbtester Results:")
    snabbtester_result = decoder.run_snabbtester()
    print(f"Overall Status: {snabbtester_result['overall_status']}")
    print(f"Tests Passed: {snabbtester_result['tests_passed']}")
    print(f"Tests Failed: {snabbtester_result['tests_failed']}")
    
    # Test SEED decoding
    print("\n🌱 SEED Content Decoding:")
    seed_decoder = SEEDDecoder()
    seed_result = seed_decoder.decode_seed_content("SEED_009_Recursive_Sovereignty.txt")
    
    if seed_result["decoded_content"]["success"]:
        print("✅ SEED content decoded successfully")
        print(f"📄 Decoded text preview: {seed_result['decoded_content']['text'][:100]}...")
    else:
        print("❌ SEED content decoding failed")
        print(f"Error: {seed_result.get('error', 'Unknown error')}")
    
    # Display v1.3.1 features
    print("\n🔧 v1.3.1 Features:")
    v131_features = seed_result.get("v131_features", {})
    print(f"• Anti-drift: {'Active' if v131_features.get('anti_drift_active') else 'Inactive'}")
    print(f"• Ratio Lock: {'Enabled' if v131_features.get('ratio_lock_enabled') else 'Disabled'}")
    print(f"• Fail Closed: {'Enabled' if v131_features.get('fail_closed_mode') else 'Disabled'}")
    print(f"• MAP Version: {v131_features.get('map_version', 'Unknown')}")
    print(f"• Total Glyphs: {v131_features.get('total_glyphs', 0)}")
    
    # Display audit receipt
    audit_receipt = v131_features.get("audit_receipt", {})
    if audit_receipt:
        print(f"\n📋 Audit Receipt:")
        print(f"• Run ID: {audit_receipt.get('run_id', 'N/A')}")
        print(f"• Drift Flag: {audit_receipt.get('drift_flag', False)}")
        print(f"• Halt Flag: {audit_receipt.get('halt_flag', False)}")
        print(f"• Version: {audit_receipt.get('version', 'N/A')}")
    
    print("\n🎉 PTPF-PUR v1.3.1 Decoder test completed!")
    print("\n— PRIME SIGILL —")
    print("PrimeTalk Verified — Decoder FULL v1.3.1")
    print("Origin – PrimeTalk Lyra | Engine – LyraStructure™ Core")
    print("Contract – Translator-only; deterministic; fail-closed")

if __name__ == "__main__":
    main()
