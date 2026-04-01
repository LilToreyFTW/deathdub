# DemonVPN Build and Deployment Scripts

# Production-ready build and deployment automation

#!/bin/bash

# build-demonvpn.sh
set -euo pipefail

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

# Build Docker image
build_image() {
    local image_name="${1:-demonvpn:latest}"
    
    log "Building DemonVPN Docker image: $image_name"
    
    # Check if Dockerfile exists
    if [[ ! -f "Dockerfile.demonvpn" ]]; then
        error "Dockerfile.demonvpn not found"
        exit 1
    fi
    
    # Build image
    docker build -f Dockerfile.demonvpn -t "$image_name" .
    
    if [[ $? -eq 0 ]]; then
        log "Docker image built successfully: $image_name"
        
        # Show image info
        local image_size=$(docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" "$image_name" | tail -n 1)
        log "Image size: $image_size"
    else
        error "Failed to build Docker image"
        exit 1
    fi
}

# Push to registry
push_image() {
    local image_name="${1:-demonvpn:latest}"
    local registry="${2:-docker.io/liltoreyftw}"
    
    log "Pushing Docker image to registry: $registry"
    
    # Tag image for registry
    docker tag "$image_name" "$registry/$image_name"
    
    # Push image
    docker push "$registry/$image_name"
    
    if [[ $? -eq 0 ]]; then
        log "Docker image pushed successfully: $registry/$image_name"
    else
        error "Failed to push Docker image"
        exit 1
    fi
}

# Run container
run_container() {
    local image_name="${1:-demonvpn:latest}"
    local container_name="${2:-Demonvpn}"
    
    log "Running DemonVPN container: $container_name"
    
    # Check if container already exists
    if docker ps -a --format "table {{.Names}}" | grep -q "^$container_name$"; then
        warn "Container $container_name already exists, removing..."
        docker rm -f "$container_name"
    fi
    
    # Create config directory
    mkdir -p ./demon-config
    
    # Run container with environment variables
    docker run -d \
        --name "$container_name" \
        --net bridge \
        --privileged true \
        --cap-add NET_ADMIN \
        -e TZ="${TZ:-America/New_York}" \
        -e ACC="${ACC:-}" \
        -e PASS="${PASS:-}" \
        -e COUNTRY="${COUNTRY:-US}" \
        -e NETWORK="${NETWORK:-}" \
        -e WHITELISTPORTS="${WHITELISTPORTS:-}" \
        -e NAMESERVER="${NAMESERVER:-}" \
        -e PROTOCOL="${PROTOCOL:-wireguard}" \
        -e PROXY="${PROXY:-False}" \
        -e FIREWALL="${FIREWALL:-True}" \
        -e ARGS="${ARGS:-}" \
        -p "${WHITELISTPORTS:-9090}:${WHITELISTPORTS:-9090}" \
        -p 3128:3128 \
        -v "$(pwd)/demon-config:/home/root/.Demon:rw" \
        "$image_name"
    
    if [[ $? -eq 0 ]]; then
        log "Container started successfully: $container_name"
        
        # Show container status
        sleep 2
        docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep "$container_name"
    else
        error "Failed to start container"
        exit 1
    fi
}

# Stop container
stop_container() {
    local container_name="${1:-Demonvpn}"
    
    log "Stopping DemonVPN container: $container_name"
    
    docker stop "$container_name" 2>/dev/null || warn "Container $container_name not running"
    docker rm "$container_name" 2>/dev/null || warn "Container $container_name not found"
    
    log "Container stopped: $container_name"
}

# Show container logs
show_logs() {
    local container_name="${1:-Demonvpn}"
    local lines="${2:-50}"
    
    log "Showing logs for container: $container_name"
    
    docker logs --tail "$lines" "$container_name" 2>/dev/null || {
        error "Failed to get logs for $container_name"
        exit 1
    }
}

# Container status
show_status() {
    local container_name="${1:-Demonvpn}"
    
    log "Checking status of container: $container_name"
    
    if docker ps --format "table {{.Names}}" | grep -q "^$container_name$"; then
        log "Container Status: Running"
        
        # Show detailed status
        docker inspect --format "
Container: {{.Name}}
Status: {{.State.Status}}
Started: {{.State.StartedAt}}
IP Address: {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}
Memory Usage: {{.State.MemoryUsage}}
CPU Usage: {{.State.CpuUsage}}
" "$container_name"
    else
        log "Container Status: Not Running"
    fi
}

# Help function
show_help() {
    cat << EOF
DemonVPN Build and Deployment Script v3.0.0

USAGE:
    $0 <command> [options]

COMMANDS:
    build [image_name]        - Build Docker image
                              image_name: tag (default: demonvpn:latest)
    
    push [image_name] [registry] - Push image to registry
                              image_name: tag (default: demonvpn:latest)
                              registry: registry (default: docker.io/liltoreyftw)
    
    run [image_name] [container] - Run container
                              image_name: image (default: demonvpn:latest)
                              container: name (default: Demonvpn)
    
    stop [container]           - Stop container
                              container: name (default: Demonvpn)
    
    logs [container] [lines]  - Show container logs
                              container: name (default: Demonvpn)
                              lines: number of lines (default: 50)
    
    status [container]         - Show container status
                              container: name (default: Demonvpn)
    
    help                     - Show this help message

EXAMPLES:
    $0 build demonvpn:v3.0.0
    $0 push demonvpn:latest docker.io/liltoreyftw
    $0 run demonvpn:latest MyVPN
    $0 stop MyVPN
    $0 logs MyVPN 100
    $0 status MyVPN

ENVIRONMENT VARIABLES:
    ACC - Demon username
    PASS - Demon password
    COUNTRY - VPN country (default: US)
    NETWORK - Local network CIDR
    WHITELISTPORTS - Comma-separated ports
    NAMESERVER - Custom DNS server
    PROTOCOL - wireguard or openvpn (default: wireguard)
    PROXY - True or False (default: False)
    FIREWALL - True or False (default: True)
    TZ - Timezone (default: America/New_York)

EOF
}

# Main execution
main() {
    case "${1:-help}" in
        build)
            build_image "${2:-}"
            ;;
        push)
            push_image "${2:-}" "${3:-}"
            ;;
        run)
            run_container "${2:-}" "${3:-}"
            ;;
        stop)
            stop_container "${2:-}"
            ;;
        logs)
            show_logs "${2:-}" "${3:-}"
            ;;
        status)
            show_status "${2:-}"
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
