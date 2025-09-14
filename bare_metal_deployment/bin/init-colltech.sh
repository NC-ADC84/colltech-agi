#!/bin/bash
# CollTech-AGI Advanced Bare Metal Init Script
# Architecture: x86_64

set -e

# Configuration
COLLTECH_HOME="/opt/colltech-agi"
COLLTECH_USER="colltech"
COLLTECH_GROUP="colltech"
LOG_FILE="/var/log/colltech-agi/init.log"

# Create log directory
mkdir -p /var/log/colltech-agi

# Log function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

log "Starting CollTech-AGI Advanced initialization..."

# Create user and group
if ! id "$COLLTECH_USER" &>/dev/null; then
    useradd -r -s /bin/false -d "$COLLTECH_HOME" "$COLLTECH_USER"
    log "Created user: $COLLTECH_USER"
fi

# Create directories
mkdir -p "$COLLTECH_HOME"/{bin,lib,etc,var,log}
mkdir -p "$COLLTECH_HOME"/var/{data,cache,logs}
chown -R "$COLLTECH_USER:$COLLTECH_GROUP" "$COLLTECH_HOME"

# Set permissions
chmod 755 "$COLLTECH_HOME"
chmod 755 "$COLLTECH_HOME"/bin
chmod 644 "$COLLTECH_HOME"/etc/*

# Install systemd services
if command -v systemctl &> /dev/null; then
    cp "$COLLTECH_HOME"/systemd/system/*.service /etc/systemd/system/
    systemctl daemon-reload
    systemctl enable colltech-agi
    systemctl enable colltech-api
    log "Systemd services installed and enabled"
fi

# Hardware detection and optimization
"$COLLTECH_HOME"/bin/detect-hardware.sh
"$COLLTECH_HOME"/bin/optimize-performance.sh

log "CollTech-AGI Advanced initialization completed successfully"
