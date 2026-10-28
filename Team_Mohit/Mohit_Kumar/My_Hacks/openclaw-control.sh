#!/usr/bin/env bash

PROJECT_DIR="/home/master/Agentic AI Programme/openclaw"

show_help() {
    echo "Usage: openclaw-control [command]"
    echo ""
    echo "Commands:"
    echo "  status     View running container status"
    echo "  chat       Launch interactive CLI session"
    echo "  logs       Stream live logs"
    echo "  health     Verify daemon health"
    echo "  stop       Stop the gateway"
    echo "  start      Start the gateway"
    echo "  restart    Restart the gateway container"
    echo "  help       Show this help message"
    echo ""
}

# Handle help first so it works independent of Docker/directory status
case "$1" in
    help|--help|-h|"")
        show_help
        exit 0
        ;;
esac

# Check if directory exists before navigating
if [ ! -d "$PROJECT_DIR" ]; then
    echo "Error: Directory '$PROJECT_DIR' does not exist." >&2
    exit 1
fi

cd "$PROJECT_DIR" || { echo "Error: Could not enter '$PROJECT_DIR'" >&2; exit 1; }

case "$1" in
    status)
        docker compose ps
        ;;
    chat)
        docker compose exec -it openclaw-gateway node dist/index.js chat
        ;;
    logs)
        docker compose logs -f openclaw-gateway
        ;;
    health)
        docker compose exec openclaw-gateway sh -lc 'node dist/index.js health --token "$OPENCLAW_GATEWAY_TOKEN"'
        ;;
    stop)
        echo "Stopping OpenClaw Gateway..."
        docker compose down
        ;;
    start)
        echo "Starting OpenClaw Gateway..."
        docker compose up -d
        echo "OpenClaw Gateway started. Dashboard: http://127.0.0.1:18789"
        ;;
    restart)
        echo "Restarting OpenClaw Gateway..."
        docker compose restart
        ;;
    *)
        echo "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
