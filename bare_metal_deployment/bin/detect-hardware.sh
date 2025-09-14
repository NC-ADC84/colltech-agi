#!/bin/bash
# CollTech-AGI Hardware Detection Script

LOG_FILE="/var/log/colltech-agi/hardware.log"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

log "Detecting hardware configuration..."

# CPU detection
CPU_MODEL=$(lscpu | grep "Model name" | cut -d: -f2 | xargs)
CPU_CORES=$(nproc)
CPU_ARCH=$(uname -m)
log "CPU: $CPU_MODEL ($CPU_CORES cores, $CPU_ARCH)"

# Memory detection
MEMORY_TOTAL=$(free -h | grep "Mem:" | awk '{print $2}')
MEMORY_AVAILABLE=$(free -h | grep "Mem:" | awk '{print $7}')
log "Memory: $MEMORY_TOTAL total, $MEMORY_AVAILABLE available"

# Storage detection
STORAGE_INFO=$(df -h / | tail -1 | awk '{print $2 " total, " $4 " available"}')
log "Storage: $STORAGE_INFO"

# Network detection
NETWORK_INTERFACES=$(ip link show | grep -E "^[0-9]+:" | cut -d: -f2 | tr -d ' ')
log "Network interfaces: $NETWORK_INTERFACES"

# GPU detection
if command -v nvidia-smi &> /dev/null; then
    GPU_INFO=$(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits | head -1)
    log "GPU: $GPU_INFO"
elif command -v lspci &> /dev/null; then
    GPU_INFO=$(lspci | grep -i vga | head -1)
    log "GPU: $GPU_INFO"
fi

# Create hardware configuration
cat > /opt/colltech-agi/etc/hardware.conf << EOF
# CollTech-AGI Hardware Configuration
CPU_MODEL="$CPU_MODEL"
CPU_CORES=$CPU_CORES
CPU_ARCH="$CPU_ARCH"
MEMORY_TOTAL="$MEMORY_TOTAL"
MEMORY_AVAILABLE="$MEMORY_AVAILABLE"
STORAGE_INFO="$STORAGE_INFO"
NETWORK_INTERFACES="$NETWORK_INTERFACES"
GPU_INFO="$GPU_INFO"
DETECTION_DATE="$(date -Iseconds)"
EOF

log "Hardware detection completed"
