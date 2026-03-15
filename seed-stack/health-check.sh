#!/usr/bin/env bash
set -uo pipefail

# Anchor Seed Stack — Health Check
#
# Checks service status and highlights what's running vs. what's not configured.
# The warnings are intentional — they show the gap between "running" and
# "production-grade."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PASS=0
WARN=0
FAIL=0

echo ""
echo "Anchor Seed Stack — Health Check"
echo "══════════════════════════════════"

# ------------------------------------------------------------------
# Service checks
# ------------------------------------------------------------------

check_service() {
    local name=$1
    local url=$2
    local display=$3

    if curl -sf --max-time 5 "$url" >/dev/null 2>&1; then
        printf "[PASS] %-20s responding\n" "$display"
        ((PASS++))
    else
        printf "[FAIL] %-20s not responding\n" "$display"
        ((FAIL++))
    fi
}

# Check if containers are even running
if ! docker compose ps --format '{{.Name}}' 2>/dev/null | grep -q .; then
    echo "[FAIL] No containers running. Run ./setup.sh first."
    echo "══════════════════════════════════"
    exit 1
fi

check_service "pihole" "http://localhost/admin/" "Pi-hole .........."
check_service "vaultwarden" "http://localhost:8080/" "Vaultwarden ......"
check_service "uptime-kuma" "http://localhost:3001/" "Uptime Kuma ......"

echo ""

# ------------------------------------------------------------------
# Configuration checks (these are supposed to warn)
# ------------------------------------------------------------------

# Backup check — is there any backup mechanism?
if crontab -l 2>/dev/null | grep -qi "backup\|docker.*cp\|sqlite3.*\.backup" || \
   systemctl list-timers 2>/dev/null | grep -qi "backup"; then
    printf "[PASS] %-20s configured\n" "Backups .........."
    ((PASS++))
else
    printf "[WARN] %-20s not configured\n" "Backups .........."
    echo "       Your data lives in Docker volumes. If the disk dies, it's gone."
    echo "       Guide: https://github.com/awesome-selfhosted/awesome-selfhosted"
    ((WARN++))
fi

# SSH hardening check
if [ -f /etc/ssh/sshd_config ]; then
    if grep -qi "PasswordAuthentication no" /etc/ssh/sshd_config /etc/ssh/sshd_config.d/*.conf 2>/dev/null; then
        printf "[PASS] %-20s key-only SSH\n" "SSH hardening ...."
        ((PASS++))
    else
        printf "[WARN] %-20s password auth still enabled\n" "SSH hardening ...."
        echo "       Anyone who can guess your password can log in."
        ((WARN++))
    fi
else
    printf "[WARN] %-20s could not check\n" "SSH hardening ...."
    ((WARN++))
fi

# Firewall check
if command -v ufw &>/dev/null && ufw status 2>/dev/null | grep -q "Status: active"; then
    printf "[PASS] %-20s UFW active\n" "Firewall ........."
    ((PASS++))
elif command -v nft &>/dev/null && nft list ruleset 2>/dev/null | grep -q "chain"; then
    printf "[PASS] %-20s nftables active\n" "Firewall ........."
    ((PASS++))
else
    printf "[WARN] %-20s not configured\n" "Firewall ........."
    echo "       All ports on this machine are exposed to your network."
    ((WARN++))
fi

# Automatic updates check
if systemctl is-active --quiet unattended-upgrades 2>/dev/null || \
   systemctl is-active --quiet apt-daily.timer 2>/dev/null; then
    printf "[PASS] %-20s enabled\n" "Auto updates ....."
    ((PASS++))
else
    printf "[WARN] %-20s not configured\n" "Auto updates ....."
    echo "       Security patches won't install themselves."
    ((WARN++))
fi

# Vaultwarden signups check
if [ -f .env ]; then
    if grep -q "SIGNUPS_ALLOWED=false" .env; then
        printf "[PASS] %-20s signups disabled\n" "Vault lockdown ..."
        ((PASS++))
    else
        printf "[WARN] %-20s signups still open\n" "Vault lockdown ..."
        echo "       Anyone on your network can create a Vaultwarden account."
        echo "       Fix: set SIGNUPS_ALLOWED=false in .env and run: docker compose up -d"
        ((WARN++))
    fi
fi

echo ""
echo "══════════════════════════════════"
echo "${PASS} passed, ${WARN} warnings, ${FAIL} failed"
echo ""

if [ $WARN -gt 0 ]; then
    echo "The warnings above are the gap between \"running\" and \"production-grade.\""
    echo "You can fix them yourself, or see what managed support looks like:"
    echo "  → Run the Proposal Generator: cd ../proposal-generator && python app.py"
    echo ""
fi

exit $FAIL
