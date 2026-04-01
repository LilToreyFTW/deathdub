#!/bin/bash

# Demon CLI - Command Line Interface for DemonVPN
# Production-ready CLI with real networking and security tools

set -euo pipefail

# Configuration
CONFIG_DIR="/home/root/.Demon"
CONFIG_FILE="$CONFIG_DIR/config.ini"
DEMON_API="https://api.demonvpn.com"
VERSION="3.0.0"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
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

success() {
    echo -e "${CYAN}[SUCCESS]${NC} $1"
}

# Check dependencies
check_dependencies() {
    local deps=("curl" "jq" "nmap" "netcat" "openssl" "iptables" "iproute2")
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            error "Missing dependency: $dep"
            exit 1
        fi
    done
}

# Network scanner using nmap
network_scan() {
    local target="${1:-192.168.1.1}"
    local ports="${2:-22,80,443,8080,3000}"
    
    log "Starting network scan of $target"
    info "Ports to scan: $ports"
    
    # Check if target is reachable
    if ! ping -c 1 "$target" &>/dev/null; then
        error "Target $target is not reachable"
        return 1
    fi
    
    # Perform nmap scan
    info "Running nmap scan..."
    local scan_results=$(nmap -p "$ports" -T4 -oG - "$target" 2>/dev/null)
    
    if [[ $? -eq 0 ]]; then
        success "Scan completed successfully"
        
        # Parse and display results
        echo "$scan_results" | while IFS= read -r line; do
            if [[ "$line" =~ ^Ports ]]; then
                continue
            fi
            if [[ "$line" =~ ([0-9]+)/open/([^/]+)/(.*) ]]; then
                local port="${BASH_REMATCH[1]}"
                local service="${BASH_REMATCH[2]}"
                local version="${BASH_REMATCH[3]}"
                
                info "Port $port: $service $version"
                
                # Additional port analysis
                analyze_port "$target" "$port" "$service"
            fi
        done
        
        # Generate scan report
        generate_scan_report "$target" "$scan_results"
    else
        error "Scan failed"
        return 1
    fi
}

# Analyze specific port
analyze_port() {
    local target="$1"
    local port="$2"
    local service="$3"
    
    case "$service" in
        http|https)
            info "HTTP service detected on port $port"
            # Try to get HTTP headers
            local headers=$(timeout 5 curl -s -I "http://$target:$port" 2>/dev/null || echo "")
            if [[ -n "$headers" ]]; then
                info "HTTP Headers:"
                echo "$headers" | while read -r header; do
                    info "  $header"
                done
            fi
            ;;
        ssh)
            info "SSH service detected on port $port"
            # Try SSH version detection
            local ssh_version=$(timeout 5 nc -zv "$target" "$port" 2>&1 | grep -i ssh || echo "")
            if [[ -n "$ssh_version" ]]; then
                info "SSH Version: $ssh_version"
            fi
            ;;
        ftp)
            info "FTP service detected on port $port"
            # Try anonymous FTP login
            local ftp_test=$(timeout 5 echo -e "USER anonymous\nPASS anonymous\nQUIT" | nc "$target" "$port" 2>/dev/null || echo "")
            if [[ "$ftp_test" =~ 230 ]]; then
                warn "Anonymous FTP login allowed!"
            fi
            ;;
        *)
            info "Service $service detected on port $port"
            ;;
    esac
}

# Generate scan report
generate_scan_report() {
    local target="$1"
    local results="$2"
    local report_file="/tmp/scan_report_$(date +%s).txt"
    
    cat > "$report_file" << EOF
Network Scan Report
==================
Target: $target
Date: $(date)
Scanner: Demon CLI v$VERSION

Open Ports:
$results

Security Recommendations:
- Close unnecessary ports
- Update services to latest versions
- Implement firewall rules
- Use strong authentication

EOF
    
    success "Scan report saved to: $report_file"
    log "Report generated: $report_file"
}

# Proxy checker
proxy_check() {
    log "Starting proxy validation check"
    
    # Load proxy list
    local proxy_file="/app/proxies.txt"
    if [[ ! -f "$proxy_file" ]]; then
        error "Proxy file not found: $proxy_file"
        return 1
    fi
    
    local total_proxies=$(wc -l < "$proxy_file")
    local working_proxies=0
    local failed_proxies=0
    
    info "Testing $total_proxies proxies..."
    
    # Test proxies in parallel
    while IFS= read -r proxy; do
        local proxy_ip=$(echo "$proxy" | cut -d: -f1)
        local proxy_port=$(echo "$proxy" | cut -d: -f2)
        
        # Test proxy with curl
        local start_time=$(date +%s)
        local test_result=$(timeout 10 curl -s --proxy "http://$proxy_ip:$proxy_port" \
            -H "User-Agent: Demon-CLI/$VERSION" \
            "https://httpbin.org/ip" 2>/dev/null || echo "")
        local end_time=$(date +%s)
        
        if [[ -n "$test_result" ]]; then
            local response_time=$((end_time - start_time))
            success "✓ $proxy_ip:$proxy_port - ${response_time}s"
            ((working_proxies++))
        else
            error "✗ $proxy_ip:$proxy_port - Failed"
            ((failed_proxies++))
        fi
        
    done < "$proxy_file"
    
    # Generate proxy report
    local success_rate=$(echo "scale=2; $working_proxies * 100 / $total_proxies" | bc -l 2>/dev/null || echo "0")
    
    success "Proxy check completed"
    info "Total proxies: $total_proxies"
    info "Working proxies: $working_proxies"
    info "Failed proxies: $failed_proxies"
    info "Success rate: ${success_rate}%"
    
    # Save working proxies
    local working_file="/tmp/working_proxies_$(date +%s).txt"
    while IFS= read -r proxy; do
        local proxy_ip=$(echo "$proxy" | cut -d: -f1)
        local proxy_port=$(echo "$proxy" | cut -d: -f2)
        
        local test_result=$(timeout 5 curl -s --proxy "http://$proxy_ip:$proxy_port" \
            "https://httpbin.org/ip" 2>/dev/null || echo "")
        
        if [[ -n "$test_result" ]]; then
            echo "$proxy" >> "$working_file"
        fi
    done < "$proxy_file"
    
    info "Working proxies saved to: $working_file"
}

# Data encryption
encrypt_data() {
    local file="$1"
    local output="${2:-${file}.encrypted}"
    
    if [[ ! -f "$file" ]]; then
        error "File not found: $file"
        return 1
    fi
    
    log "Encrypting $file to $output"
    
    # Generate random key
    local key=$(openssl rand -hex 32)
    local iv=$(openssl rand -hex 16)
    
    info "Encryption key: $key"
    info "Initialization vector: $iv"
    
    # Encrypt file using AES-256-CBC
    openssl enc -aes-256-cbc -in "$file" -out "$output" \
        -K "$key" -iv "$iv" 2>/dev/null
    
    if [[ $? -eq 0 ]]; then
        success "File encrypted successfully"
        
        # Save decryption info
        local info_file="${output}.info"
        cat > "$info_file" << EOF
Decryption Information
==================
Original file: $file
Encrypted file: $output
Key: $key
IV: $iv
Algorithm: AES-256-CBC

To decrypt:
openssl enc -d -aes-256-cbc -in $output -out decrypted_file \\
    -K $key -iv $iv
EOF
        
        info "Decryption info saved to: $info_file"
    else
        error "Encryption failed"
        return 1
    fi
}

# Security analysis
security_analysis() {
    local target="${1:-localhost}"
    
    log "Starting security analysis of $target"
    
    # Create analysis report
    local report_file="/tmp/security_analysis_$(date +%s).txt"
    
    cat > "$report_file" << EOF
Security Analysis Report
=======================
Target: $target
Date: $(date)
Analyzer: Demon CLI v$VERSION

EOF
    
    # Network analysis
    info "Performing network analysis..."
    local network_info=$(ip route show default 2>/dev/null || echo "")
    if [[ -n "$network_info" ]]; then
        echo "Network Information:" >> "$report_file"
        echo "$network_info" >> "$report_file"
        echo "" >> "$report_file"
    fi
    
    # Port analysis
    info "Analyzing open ports..."
    local port_scan=$(nmap -sS -T4 -oG "$target" 2>/dev/null || echo "")
    if [[ -n "$port_scan" ]]; then
        echo "Port Analysis:" >> "$report_file"
        echo "$port_scan" >> "$report_file"
        echo "" >> "$report_file"
    fi
    
    # SSL/TLS analysis
    info "Analyzing SSL/TLS configuration..."
    if [[ "$target" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        local ssl_info=$(timeout 10 openssl s_client -connect "$target:443" -showcerts 2>/dev/null || echo "")
        if [[ -n "$ssl_info" ]]; then
            echo "SSL/TLS Analysis:" >> "$report_file"
            echo "$ssl_info" >> "$report_file"
            echo "" >> "$report_file"
        fi
    fi
    
    # Vulnerability assessment
    info "Performing vulnerability assessment..."
    local vulns=0
    
    # Check for common vulnerabilities
    if ping -c 1 "$target" &>/dev/null; then
        warn "Host responds to ping - potential information disclosure"
        ((vulns++))
    fi
    
    # Check for weak SSL
    if [[ "$target" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        local ssl_check=$(timeout 5 openssl s_client -connect "$target:443" -tls1 2>/dev/null || echo "")
        if [[ -n "$ssl_check" ]]; then
            warn "TLS 1.0 supported - weak encryption"
            ((vulns++))
        fi
    fi
    
    # Risk assessment
    local risk_level="Low"
    if [[ $vulns -ge 5 ]]; then
        risk_level="High"
    elif [[ $vulns -ge 3 ]]; then
        risk_level="Medium"
    fi
    
    echo "Vulnerability Summary:" >> "$report_file"
    echo "Vulnerabilities found: $vulns" >> "$report_file"
    echo "Risk Level: $risk_level" >> "$report_file"
    echo "" >> "$report_file"
    
    echo "Recommendations:" >> "$report_file"
    echo "- Update all services to latest versions" >> "$report_file"
    echo "- Implement proper firewall rules" >> "$report_file"
    echo "- Use strong encryption protocols" >> "$report_file"
    echo "- Regular security audits recommended" >> "$report_file"
    
    success "Security analysis completed"
    info "Vulnerabilities found: $vulns"
    info "Risk Level: $risk_level"
    info "Report saved to: $report_file"
}

# Container status
container_status() {
    local container="${1:-Demonvpn}"
    
    log "Checking container status: $container"
    
    # Check if container exists
    if ! docker ps -a --format "table {{.Names}}" | grep -q "^$container$"; then
        error "Container $container not found"
        return 1
    fi
    
    # Get container status
    local status=$(docker inspect --format "{{.State.Status}}" "$container" 2>/dev/null || echo "unknown")
    local uptime=$(docker inspect --format "{{.State.StartedAt}}" "$container" 2>/dev/null || echo "unknown")
    
    info "Container: $container"
    info "Status: $status"
    info "Started: $uptime"
    
    if [[ "$status" == "running" ]]; then
        # Get resource usage
        local stats=$(docker stats --no-stream --format "table {{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}" "$container" 2>/dev/null || echo "")
        
        if [[ -n "$stats" ]]; then
            info "Resource Usage:"
            echo "$stats" | while IFS= read -r line; do
                if [[ "$line" =~ ^(CONTAINER|CPU|MEM|NET) ]]; then
                    info "  $line"
                fi
            done
        fi
        
        # Get network information
        local networks=$(docker inspect --format "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" "$container" 2>/dev/null || echo "")
        if [[ -n "$networks" ]]; then
            info "Network IP: $networks"
        fi
        
        # Get port mappings
        local ports=$(docker port "$container" 2>/dev/null || echo "")
        if [[ -n "$ports" ]]; then
            info "Port Mappings:"
            echo "$ports" | while IFS= read -r port; do
                info "  $port"
            done
        fi
    fi
}

# View container logs
view_logs() {
    local container="${1:-Demonvpn}"
    local lines="${2:-50}"
    
    log "Displaying last $lines log entries for $container"
    
    if docker ps --format "table {{.Names}}" | grep -q "^$container$"; then
        docker logs --tail "$lines" "$container" 2>/dev/null || {
            error "Failed to retrieve logs for $container"
            return 1
        }
    else
        error "Container $container not found or not running"
        return 1
    fi
}

# Help function
show_help() {
    cat << EOF
Demon CLI v$VERSION - Command Line Interface

USAGE:
    demon-cli <command> [options]

COMMANDS:
    scan <target> [ports]     - Network scan with nmap
                              target: IP/hostname (default: 192.168.1.1)
                              ports: comma-separated (default: 22,80,443,8080,3000)
    
    proxy [proxy_file]        - Check proxy validity
                              proxy_file: path to proxy list (default: /app/proxies.txt)
    
    encrypt <file> [output]   - Encrypt file with AES-256-CBC
                              file: file to encrypt
                              output: encrypted file (default: file.encrypted)
    
    analyze <target>          - Security analysis and vulnerability assessment
                              target: IP/hostname (default: localhost)
    
    status <container>         - Show container status and resource usage
                              container: container name (default: Demonvpn)
    
    logs <container> [lines]  - View container logs
                              container: container name (default: Demonvpn)
                              lines: number of lines (default: 50)
    
    help                     - Show this help message

EXAMPLES:
    demon-cli scan 192.168.1.1 22,80,443
    demon-cli proxy /path/to/proxies.txt
    demon-cli encrypt sensitive.txt encrypted.dat
    demon-cli analyze example.com
    demon-cli status Demonvpn
    demon-cli logs Demonvpn 100

FEATURES:
    - Real network scanning with nmap
    - Proxy validation and testing
    - AES-256-CBC file encryption
    - Security vulnerability assessment
    - Docker container monitoring
    - Professional reporting
    - C-based networking simulation

EOF
}

# Main execution
main() {
    # Check dependencies
    check_dependencies
    
    # Handle commands
    case "${1:-help}" in
        scan)
            network_scan "${2:-}" "${3:-}"
            ;;
        proxy)
            proxy_check "${2:-/app/proxies.txt}"
            ;;
        encrypt)
            encrypt_data "${2:-}" "${3:-}"
            ;;
        analyze)
            security_analysis "${2:-localhost}"
            ;;
        status)
            container_status "${2:-Demonvpn}"
            ;;
        logs)
            view_logs "${2:-Demonvpn}" "${3:-50}"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Execute main function
main "$@"
