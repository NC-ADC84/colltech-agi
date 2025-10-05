# CollTech-AGI Installation Guide

## Quick Installation

### Option 1: Development Install (Recommended)

Install in development mode to allow editing:

```bash
cd colltech-agi
pip install -e .
```

### Option 2: Standard Install

Install as a regular package:

```bash
cd colltech-agi
pip install .
```

### Option 3: Install with Development Tools

Install with testing and development dependencies:

```bash
cd colltech-agi
pip install -e ".[dev]"
```

## Verification

After installation, verify it works:

```bash
# Check version
python -c "import colltech_agi; print(colltech_agi.__version__)"

# Run interactive CLI
python -m colltech_agi_cli

# Or if console script is installed
colltech-agi
```

## Usage

### Interactive Mode

```bash
# Start interactive session
python colltech-agi/colltech_agi_cli.py

# Or if installed
colltech-agi
```

### Python API

```python
from colltech_agi import (
    AgenticMindsetsIntegration,
    AgenticConfig,
    AgenticMode,
    PersonalitySystem,
    PersonalityProfile
)

# Create integration
agentic = AgenticMindsetsIntegration()

# Process input
result = agentic.process_with_agentic_mindset(
    "What is consciousness?",
    mode=AgenticMode.CONSCIOUS
)

print(result['processed_prompt'])
```

### Simple Demo

```bash
cd colltech-agi/examples
python agentic_mindsets_demo.py
```

### Comprehensive Tests

```bash
cd colltech-agi/examples
python comprehensive_agentic_test.py
```

## System Requirements

- **Python**: 3.8 or higher
- **Dependencies**: None (pure Python standard library)
- **OS**: Windows, macOS, Linux

## Directory Structure

```
colltech-agi/
├── __init__.py                          # Package initialization
├── setup.py                             # Installation script
├── colltech_agi_cli.py                  # CLI interface
├── src/
│   └── agentic_mindsets_integration.py  # Integration module
├── examples/
│   ├── agentic_mindsets_demo.py         # Simple demo
│   └── comprehensive_agentic_test.py    # Test suite
└── AGENTIC_MINDSETS_INTEGRATION_GUIDE.md
```

## Troubleshooting

### Import Errors

If you get import errors:

```bash
# Ensure you're in the correct directory
cd colltech-agi

# Reinstall in development mode
pip install -e .
```

### Path Issues

If AgenticMindsets can't be found:

```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../AgenticMindsets'))
```

### Module Not Found

If `colltech_agi` module is not found after installation:

```bash
# Check if it's installed
pip list | grep colltech

# Reinstall
pip uninstall colltech-agi
pip install -e .
```

## Uninstallation

```bash
pip uninstall colltech-agi
```

## Development Setup

For development:

```bash
# Clone/navigate to directory
cd colltech-agi

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests
python examples/comprehensive_agentic_test.py

# Run demos
python examples/agentic_mindsets_demo.py
```

## Next Steps

After installation:

1. Read `AGENTIC_MINDSETS_INTEGRATION_GUIDE.md` for usage examples
2. Try the interactive CLI: `python colltech_agi_cli.py`
3. Run the demos in `examples/`
4. Explore the five agentic modes
5. Integrate into your projects

## Support

For issues or questions:
- Check `AGENTIC_MINDSETS_INTEGRATION_GUIDE.md`
- Review `AgenticMindsets/README.md`
- Run comprehensive tests to verify installation

## License

See LICENSE file for details.
