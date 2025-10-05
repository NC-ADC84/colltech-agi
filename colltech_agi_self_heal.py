"""
Self-Heal Manager for CollTech-AGI

Provides lightweight health checks and safe, local repair actions.
This module performs non-destructive checks (imports, backend init, filesystem access)
and offers conservative repair steps (re-initialize components, reset allowlist,
clear caches). It deliberately avoids running external downloads or executing
untrusted code.
"""
from typing import Dict, Any
import logging
import importlib
import traceback
from pathlib import Path
import time

logger = logging.getLogger(__name__)


class SelfHealManager:
    def __init__(self, workspace_path: str = None):
        self.workspace_path = Path(workspace_path) if workspace_path else Path.cwd()

    def check_imports(self) -> Dict[str, Any]:
        """Verify key modules can be imported."""
        checks = {}
        modules = [
            'colltech_agi_enhanced_backend',
            'colltech_agi_expanded_personalities',
        ]
        for m in modules:
            try:
                importlib.import_module(m)
                checks[m] = {'ok': True}
            except Exception as e:
                checks[m] = {'ok': False, 'error': str(e)}
        return checks

    def check_backend(self) -> Dict[str, Any]:
        """Perform lightweight backend checks without mutating state."""
        try:
            from colltech_agi_enhanced_backend import EnhancedBackend
        except Exception as e:
            return {'ok': False, 'error': f'EnhancedBackend import failed: {e}'}

        try:
            be = EnhancedBackend({'llm_provider': 'local'})
            # Test a harmless file-system call against home directory anchor
            test_dir = str(Path.home())
            res = be.process_message(f"/list {test_dir}")
            ok = res.get('type') == 'directory_list' and res.get('result', {}).get('success', False)
            return {'ok': bool(ok), 'details': res}
        except Exception as e:
            return {'ok': False, 'error': str(e), 'trace': traceback.format_exc()}

    def check_filesystem(self) -> Dict[str, Any]:
        """Check workspace and permissions for basic operations."""
        try:
            p = self.workspace_path
            exists = p.exists()
            can_list = any(p.iterdir()) if exists else False
            return {'ok': exists, 'path': str(p), 'can_list': can_list}
        except Exception as e:
            return {'ok': False, 'error': str(e)}

    def run_heal(self) -> Dict[str, Any]:
        """Run health checks and attempt a small set of safe repairs.

        Returns a dict summarizing checks and any repair actions taken.
        """
        summary: Dict[str, Any] = {'timestamp': time.time(), 'checks': {}, 'repairs': []}

        # 1) Imports
        summary['checks']['imports'] = self.check_imports()

        # 2) Filesystem
        summary['checks']['filesystem'] = self.check_filesystem()

        # 3) Backend
        backend_check = self.check_backend()
        summary['checks']['backend'] = backend_check

        # Conservative repairs: only if backend failed, attempt re-init and reset allowlist
        repairs = []
        if not backend_check.get('ok'):
            try:
                from colltech_agi_enhanced_backend import EnhancedBackend
                be = EnhancedBackend({'llm_provider': 'local'})
                # Reset allowlist to include drive root + common folders
                try:
                    be.file_system.allowed_directories = [
                        str(Path.home() / 'Documents'),
                        str(Path.home() / 'Desktop'),
                        str(Path.home() / 'Downloads'),
                        be.file_system.allowed_directories[ -1 ] if be.file_system.allowed_directories else str(Path(__file__).resolve().anchor)
                    ]
                    repairs.append({'action': 'reset_allowed_directories', 'result': 'ok'})
                except Exception as e:
                    repairs.append({'action': 'reset_allowed_directories', 'result': f'failed: {e}'})

                # Try a simple backend re-init check
                try:
                    res = be.process_message(f"/list {str(Path.home())}")
                    repairs.append({'action': 'backend_reinit_check', 'result': res})
                except Exception as e:
                    repairs.append({'action': 'backend_reinit_check', 'result': f'failed: {e}'})

            except Exception as e:
                repairs.append({'action': 'backend_repair', 'result': f'failed to import EnhancedBackend: {e}'})

        summary['repairs'] = repairs
        return summary

    def save_report(self, report: Dict[str, Any], filename: str = None) -> str:
        """Save diagnostics report as JSON into the workspace path and return the file path."""
        try:
            import json
            ts = int(time.time())
            fname = filename or f"colltech_diagnostics_{ts}.json"
            out_path = (self.workspace_path / fname).resolve()
            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            logger.info("Diagnostics saved to %s", out_path)
            return str(out_path)
        except Exception as e:
            logger.exception("Failed to save diagnostics: %s", e)
            raise


if __name__ == '__main__':
    # Quick CLI runner for local debugging
    mgr = SelfHealManager()
    out = mgr.run_heal()
    import json
    print(json.dumps(out, indent=2))
