#!/bin/bash
# CollTech-AGI Advanced Bare Metal Installer
# Architecture: x86_64

set -e

INSTALL_DIR="/opt/colltech-agi"
SERVICE_USER="colltech"
SERVICE_GROUP="colltech"

echo "🚀 CollTech-AGI Advanced Bare Metal Installation"
echo "================================================"
echo "Architecture: x86_64"
echo "Install Directory: $INSTALL_DIR"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run as root (use sudo)"
    exit 1
fi

# Check architecture compatibility
CURRENT_ARCH=$(uname -m)
if [ "$CURRENT_ARCH" != "x86_64" ] && [ "x86_64" != "auto" ]; then
    echo "⚠️  Warning: Target architecture (x86_64) differs from current ($CURRENT_ARCH)"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "📦 Installing CollTech-AGI Advanced..."

# Create installation directory
mkdir -p "$INSTALL_DIR"
cp -r ./* "$INSTALL_DIR/"

# Create service user
if ! id "$SERVICE_USER" &>/dev/null; then
    useradd -r -s /bin/false -d "$INSTALL_DIR" "$SERVICE_USER"
    echo "✅ Created service user: $SERVICE_USER"
fi

# Set permissions
chown -R "$SERVICE_USER:$SERVICE_GROUP" "$INSTALL_DIR"
chmod +x "$INSTALL_DIR/bin"/*

# Install systemd services
if command -v systemctl &> /dev/null; then
    cp "$INSTALL_DIR/systemd/system"/*.service /etc/systemd/system/
    systemctl daemon-reload
    systemctl enable colltech-agi
    systemctl enable colltech-api
    echo "✅ Systemd services installed and enabled"
fi

# Run initialization
"$INSTALL_DIR/bin/init-colltech.sh"

# Install Python dependencies
if command -v pip3 &> /dev/null; then
    pip3 install -r "$INSTALL_DIR/requirements.txt"
    echo "✅ Python dependencies installed"
else
    echo "⚠️  pip3 not found, please install Python dependencies manually"
fi

echo ""
echo "🎉 CollTech-AGI Advanced installation completed!"
echo ""
echo "To start the service:"
echo "  sudo systemctl start colltech-agi"
echo "  sudo systemctl start colltech-api"
echo ""
echo "To check status:"
echo "  sudo systemctl status colltech-agi"
echo "  sudo systemctl status colltech-api"
echo ""
echo "Logs are available at:"
echo "  /var/log/colltech-agi/"
echo ""
