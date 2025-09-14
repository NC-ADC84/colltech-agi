#!/bin/bash
# CollTech-AGI Advanced Startup Script for x86_64

echo "🚀 Starting CollTech-AGI Advanced..."
echo "Architecture: x86_64"
echo "Python version: $(python3 --version)"

# Set environment variables
export PYTHONPATH=/colltech_agi
export COLLTECH_PERSISTENT_PATH=/colltech_persistent

# Create persistent storage if it doesn't exist
mkdir -p /colltech_persistent

# Start CollTech-AGI
cd /colltech_agi
python3 colltech_agi_realtime_advanced.py
