#!/bin/bash

# DemonVPN WireGuard Docker Implementation
# Production-ready WireGuard client with Demon CLI integration

set -euo pipefail

# Configuration
CONFIG_DIR="/home/root/.Demon"
CONFIG_FILE="$CONFIG_DIR/config.ini"
WG_CONFIG="$CONFIG_DIR/wg0.conf"
DEMON_API="https://api.demonvpn.com"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Check dependencies
check_dependencies() {
    local deps=("wg" "wg-quick" "curl" "jq" "iptables" "iproute2")
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            error "Missing dependency: $dep"
            exit 1
        fi
    done
}

# Initialize WireGuard configuration
init_wireguard() {
    log "Initializing WireGuard configuration"
    
    # Create config directory
    mkdir -p "$CONFIG_DIR"
    
    # Get Demon servers
    local country="${COUNTRY:-US}"
    local protocol="${PROTOCOL:-wireguard}"
    
    log "Fetching Demon servers for $country"
    
    # Authenticate with Demon API
    if [[ -n "${ACC:-}" && -n "${PASS:-}" ]]; then
        log "Authenticating with Demon API..."
        local auth_response=$(curl -s -X POST \
            -H "Content-Type: application/json" \
            -d "{\"email\":\"$ACC\",\"password\":\"$PASS\"}" \
            "$DEMON_API/auth")
        
        if [[ $? -ne 0 ]]; then
            error "Failed to authenticate with Demon API"
            exit 1
        fi
        
        local token=$(echo "$auth_response" | jq -r '.token // empty')
        if [[ -z "$token" ]]; then
            error "Invalid credentials or API response"
            exit 1
        fi
        
        # Store token
        echo "token=$token" > "$CONFIG_FILE"
        
        # Fetch servers
        local servers_response=$(curl -s -H "Authorization: Bearer $token" \
            "$DEMON_API/servers?country=$country&protocol=$protocol")
        
        if [[ $? -ne 0 ]]; then
            error "Failed to fetch servers from Demon API"
            exit 1
        fi
        
        # Parse and select best server
        local server=$(echo "$servers_response" | jq -r '.servers[0] // empty')
        if [[ -z "$server" ]]; then
            error "No servers available for $country"
            exit 1
        fi
        
        local server_ip=$(echo "$server" | jq -r '.ip')
        local server_port=$(echo "$server" | jq -r '.port')
        local server_pubkey=$(echo "$server" | jq -r '.public_key')
        local client_privkey=$(wg genkey | base64 -w0)
        local client_pubkey=$(echo "$client_privkey" | base64 -d | wg pubkey)
        
        # Generate WireGuard config
        cat > "$WG_CONFIG" << EOF
[Interface]
PrivateKey = $client_privkey
Address = 10.8.0.2/24
DNS = ${NAMESERVER:-1.1.1.1}

[Peer]
PublicKey = $server_pubkey
AllowedIPs = 0.0.0.0/0
Endpoint = $server_ip:$server_port
PersistentKeepalive = 25
EOF
        
        log "WireGuard configuration generated"
        log "Server: $server_ip:$server_port"
        log "Client IP: 10.8.0.2"
        
    else
        error "ACC and PASS environment variables required"
        exit 1
    fi
}

# Setup firewall rules
setup_firewall() {
    log "Configuring firewall rules"
    
    # Enable IP forwarding
    echo 1 > /proc/sys/net/ipv4/ip_forward
    
    # Configure iptables
    iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE
    iptables -A FORWARD -s 10.8.0.0/24 -j ACCEPT
    iptables -A FORWARD -m state --state RELATED,ESTABLISHED -j ACCEPT
    
    # Allow whitelisted ports
    if [[ -n "${WHITELISTPORTS:-}" ]]; then
        IFS=',' read -ra ports <<< "$WHITELISTPORTS"
        for port in "${ports[@]}"; do
            iptables -A INPUT -p tcp --dport "$port" -j ACCEPT
            log "Whitelisted port: $port"
        done
    fi
    
    # Allow DNS during setup
    iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
    iptables -A INPUT -p udp --dport 53 -j ACCEPT
}

# Start WireGuard connection
start_vpn() {
    log "Starting WireGuard connection"
    
    # Check if already connected
    if wg show wg0 &>/dev/null; then
        warn "WireGuard already connected"
        return 0
    fi
    
    # Initialize if needed
    if [[ ! -f "$WG_CONFIG" ]]; then
        init_wireguard
        setup_firewall
    fi
    
    # Start WireGuard
    wg-quick up "$WG_CONFIG"
    
    if [[ $? -eq 0 ]]; then
        log "WireGuard connection established"
        show_connection_info
        
        # Setup proxy if requested
        if [[ "${PROXY:-}" == "True" ]]; then
            start_proxy
        fi
        
        # Block DNS after connection
        iptables -D OUTPUT -p udp --dport 53 -j ACCEPT
        iptables -D INPUT -p udp --dport 53 -j ACCEPT
        
    else
        error "Failed to start WireGuard"
        exit 1
    fi
}

# Stop VPN connection
stop_vpn() {
    log "Stopping WireGuard connection"
    
    # Stop proxy if running
    stop_proxy
    
    # Stop WireGuard
    if wg show wg0 &>/dev/null; then
        wg-quick down "$WG_CONFIG"
        log "WireGuard connection stopped"
    fi
    
    # Clear firewall rules
    iptables -t nat -F
    iptables -F
    log "Firewall rules cleared"
}

# Start HTTP proxy
start_proxy() {
    log "Starting HTTP proxy service"
    
    # Create simple proxy using squid or tinyproxy
    if command -v squid &>/dev/null; then
        systemctl enable squid
        systemctl start squid
        log "Squid proxy started on port 3128"
    elif command -v tinyproxy &>/dev/null; then
        tinyproxy -c /etc/tinyproxy/tinyproxy.conf
        log "TinyProxy started on port 3128"
    else
        warn "No proxy service available, installing tinyproxy"
        apt-get update && apt-get install -y tinyproxy
        tinyproxy -c /etc/tinyproxy/tinyproxy.conf
        log "TinyProxy installed and started on port 3128"
    fi
    
    # Allow proxy port
    iptables -A INPUT -p tcp --dport 3128 -j ACCEPT
    iptables -A OUTPUT -p tcp --dport 3128 -j ACCEPT
}

# Stop HTTP proxy
stop_proxy() {
    log "Stopping HTTP proxy service"
    
    systemctl stop squid 2>/dev/null || true
    pkill tinyproxy 2>/dev/null || true
    
    # Block proxy port
    iptables -D INPUT -p tcp --dport 3128 -j ACCEPT
    iptables -D OUTPUT -p tcp --dport 3128 -j ACCEPT
    
    log "HTTP proxy service stopped"
}

# Show connection information
show_connection_info() {
    log "Connection Information:"
    
    # Get external IP
    local external_ip=$(curl -s https://ipinfo.io/ip 2>/dev/null || echo "Unknown")
    local city=$(curl -s https://ipinfo.io/city 2>/dev/null || echo "Unknown")
    local country=$(curl -s https://ipinfo.io/country 2>/dev/null || echo "Unknown")
    local region=$(curl -s https://ipinfo.io/region 2>/dev/null || echo "Unknown")
    
    info "External IP: $external_ip"
    info "Location: $city, $region, $country"
    info "VPN Interface: wg0"
    info "VPN IP: 10.8.0.2"
    
    # Show WireGuard status
    if wg show wg0 &>/dev/null; then
        local peer_info=$(wg show wg0)
        info "Peer Status: Connected"
        info "Handshake: $(echo "$peer_info" | grep "latest handshake" | awk '{print $3}')"
        info "Transfer: $(echo "$peer_info" | grep "transfer" | awk '{print $2, $3}')"
    fi
}

# Monitor connection
monitor_connection() {
    log "Starting connection monitoring"
    
    while true; do
        sleep 30
        
        # Check if WireGuard is still up
        if ! wg show wg0 &>/dev/null; then
            warn "WireGuard connection lost, attempting reconnect..."
            stop_vpn
            sleep 5
            start_vpn
        fi
        
        # Check internet connectivity
        if ! ping -c 1 1.1.1.1 &>/dev/null; then
            warn "Internet connectivity lost, restarting VPN..."
            stop_vpn
            sleep 10
            start_vpn
        fi
        
        # Log status
        log "Connection monitoring active - $(date)"
    done
}

# Main execution
main() {
    log "DemonVPN WireGuard Docker Client v3.0.0"
    log "Created by: Tyler McPhee"
    log "GitHub: https://github.com/LilToreyFTW/deathdub"
    
    # Check dependencies
    check_dependencies
    
    # Handle commands
    case "${1:-start}" in
        start)
            start_vpn
            ;;
        stop)
            stop_vpn
            ;;
        status)
            show_connection_info
            ;;
        restart)
            stop_vpn
            sleep 2
            start_vpn
            ;;
        monitor)
            start_vpn
            monitor_connection
            ;;
        *)
            echo "Usage: $0 {start|stop|status|restart|monitor}"
            echo "  start   - Start VPN connection"
            echo "  stop    - Stop VPN connection"
            echo "  status  - Show connection status"
            echo "  restart - Restart VPN connection"
            echo "  monitor - Start with monitoring"
            exit 1
            ;;
    esac
}

# Execute main function
main "$@"
