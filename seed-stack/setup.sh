#!/usr/bin/env bash
set -euo pipefail

# Anchor Seed Stack — Setup Script
#
# This script will:
#   1. Verify Docker and Docker Compose are installed
#   2. Generate secrets if .env doesn't exist
#   3. Start the stack with docker compose up -d
#
# This script will NOT:
#   - Modify your system configuration
#   - Open firewall ports
#   - Install software (it tells you what to install if something is missing)
#   - Send any data off your machine

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "Anchor Seed Stack — Setup"
echo "========================="
echo ""
echo "This will start three services on your machine:"
echo "  - Pi-hole (DNS ad blocking)        → http://localhost/admin"
echo "  - Vaultwarden (password manager)    → http://localhost:8080"
echo "  - Uptime Kuma (service monitoring)  → http://localhost:3001"
echo ""
echo "No data is sent off your machine. No telemetry. No phone-home."
echo ""

# ------------------------------------------------------------------
# Prerequisite checks
# ------------------------------------------------------------------

MISSING=0

if ! command -v docker &>/dev/null; then
    echo "[FAIL] Docker is not installed."
    echo "       Install it: curl -fsSL https://get.docker.com | sh"
    MISSING=1
fi

if ! docker compose version &>/dev/null 2>&1; then
    echo "[FAIL] Docker Compose plugin is not available."
    echo "       Install it: sudo apt install docker-compose-plugin"
    MISSING=1
fi

if [ $MISSING -ne 0 ]; then
    echo ""
    echo "Install the missing prerequisites and run this script again."
    exit 1
fi

# Check Docker daemon is running
if ! docker info &>/dev/null 2>&1; then
    echo "[FAIL] Docker daemon is not running."
    echo "       Start it: sudo systemctl start docker"
    echo "       Or if you need to add yourself to the docker group:"
    echo "       sudo usermod -aG docker \$USER && newgrp docker"
    exit 1
fi

echo "[OK] Docker $(docker --version | grep -oP '\d+\.\d+\.\d+')"
echo "[OK] Docker Compose $(docker compose version --short)"
echo ""

# ------------------------------------------------------------------
# Environment setup
# ------------------------------------------------------------------

if [ ! -f .env ]; then
    echo "No .env file found. Creating one from .env.example..."
    echo ""

    cp .env.example .env

    # Generate secrets
    PIHOLE_PW=$(openssl rand -base64 16 | tr -d '=/+' | head -c 16)
    VAULT_TOKEN=$(openssl rand -hex 32)

    # Detect timezone
    if [ -f /etc/timezone ]; then
        DETECTED_TZ=$(cat /etc/timezone)
    elif command -v timedatectl &>/dev/null; then
        DETECTED_TZ=$(timedatectl show -p Timezone --value 2>/dev/null || echo "America/Chicago")
    else
        DETECTED_TZ="America/Chicago"
    fi

    sed -i "s|^TZ=.*|TZ=${DETECTED_TZ}|" .env
    sed -i "s|^PIHOLE_PASSWORD=.*|PIHOLE_PASSWORD=${PIHOLE_PW}|" .env
    sed -i "s|^VAULTWARDEN_ADMIN_TOKEN=.*|VAULTWARDEN_ADMIN_TOKEN=${VAULT_TOKEN}|" .env

    echo "Generated .env with:"
    echo "  Timezone:           ${DETECTED_TZ}"
    echo "  Pi-hole password:   ${PIHOLE_PW}"
    echo "  Vaultwarden token:  ${VAULT_TOKEN:0:8}... (see .env for full value)"
    echo ""
    echo "Save these somewhere safe. You'll need them to log into the admin panels."
    echo ""
else
    echo "[OK] .env file exists"
    echo ""
fi

# ------------------------------------------------------------------
# Port conflict check
# ------------------------------------------------------------------

check_port() {
    local port=$1
    local service=$2
    if ss -tlnp 2>/dev/null | grep -q ":${port} " || \
       netstat -tlnp 2>/dev/null | grep -q ":${port} "; then
        echo "[WARN] Port ${port} is already in use (needed by ${service})"
        echo "       Check what's using it: sudo lsof -i :${port}"
        return 1
    fi
    return 0
}

PORT_CONFLICT=0
check_port 53 "Pi-hole (DNS)" || PORT_CONFLICT=1
check_port 80 "Pi-hole (admin)" || PORT_CONFLICT=1
check_port 8080 "Vaultwarden" || PORT_CONFLICT=1
check_port 3001 "Uptime Kuma" || PORT_CONFLICT=1

if [ $PORT_CONFLICT -ne 0 ]; then
    echo ""
    echo "Some ports are in use. The stack may not start correctly."
    echo "Common fix: Ubuntu runs systemd-resolved on port 53."
    echo "  sudo systemctl stop systemd-resolved"
    echo "  sudo systemctl disable systemd-resolved"
    echo ""
fi

# ------------------------------------------------------------------
# Confirmation
# ------------------------------------------------------------------

read -rp "Start the Seed Stack? [y/N] " confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

echo ""

# ------------------------------------------------------------------
# Launch
# ------------------------------------------------------------------

echo "Pulling container images (this may take a few minutes on first run)..."
docker compose pull

echo ""
echo "Starting services..."
docker compose up -d

echo ""
echo "Waiting for services to start..."
sleep 5

# ------------------------------------------------------------------
# Status
# ------------------------------------------------------------------

echo ""
docker compose ps
echo ""

LOCAL_IP=$(hostname -I 2>/dev/null | awk '{print $1}' || echo "YOUR_IP")

echo "========================="
echo "Setup complete!"
echo ""
echo "Access your services:"
echo "  Pi-hole admin:   http://${LOCAL_IP}/admin"
echo "  Vaultwarden:     http://${LOCAL_IP}:8080"
echo "  Uptime Kuma:     http://${LOCAL_IP}:3001"
echo ""
echo "Next steps:"
echo "  1. Log into Pi-hole and set it as your router's DNS server"
echo "  2. Create your Vaultwarden account, then set SIGNUPS_ALLOWED=false in .env"
echo "     and run: docker compose up -d"
echo "  3. Set up monitors in Uptime Kuma for your new services"
echo "  4. Run ./health-check.sh to see what else needs attention"
echo ""
