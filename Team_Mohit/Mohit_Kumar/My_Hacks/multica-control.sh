#!/usr/bin/env bash

PROJECT_DIR="/home/master/Agentic AI Programme/multica"

show_help() {
    echo "Usage: multica-control [command]"
    echo ""
    echo "Commands:"
    echo "  start        Start all services (postgres, backend, frontend, daemon)"
    echo "  stop         Stop all services"
    echo "  restart      Restart all services"
    echo "  status       View running container status"
    echo "  logs         Stream live logs (all services)"
    echo "  logs <svc>   Stream logs for a specific service (backend, frontend, daemon, postgres)"
    echo "  build        Build the daemon image"
    echo "  login        Authenticate the daemon with a personal access token"
    echo "  daemon       Show daemon status"
    echo "  health       Check backend health"
    echo "  help         Show this help message"
    echo ""
}

case "$1" in
    help|--help|-h|"")
        show_help
        exit 0
        ;;
esac

if [ ! -d "$PROJECT_DIR" ]; then
    echo "Error: Directory '$PROJECT_DIR' does not exist." >&2
    exit 1
fi

cd "$PROJECT_DIR" || { echo "Error: Could not enter '$PROJECT_DIR'" >&2; exit 1; }

case "$1" in
    start)
        echo "Starting Multica..."
        docker compose up -d
        echo ""
        echo "Frontend:  http://localhost:3000  (OTP: 888888)"
        echo "Backend:   http://localhost:8080"
        echo ""
        echo "Run 'multica-control login' to authenticate the daemon."
        ;;
    stop)
        echo "Stopping Multica..."
        docker compose down
        ;;
    restart)
        echo "Restarting Multica..."
        docker compose restart
        ;;
    status)
        docker compose ps
        ;;
    logs)
        if [ -n "$2" ]; then
            docker compose logs -f "$2"
        else
            docker compose logs -f
        fi
        ;;
    build)
        echo "Building daemon image..."
        docker compose build daemon
        ;;
    login)
        echo "Enter your personal access token (Settings → API Tokens in the web UI):"
        read -r -s TOKEN
        echo ""
        docker compose exec daemon multica config set server_url http://backend:8080
        docker compose exec daemon multica config set app_url http://localhost:3000
        docker compose exec daemon multica login --token "$TOKEN"
        echo ""
        echo "Restarting daemon to apply token..."
        docker compose up -d --no-build --force-recreate daemon
        echo "Done. Run 'multica-control daemon' to verify."
        ;;
    daemon)
        docker compose exec daemon multica daemon status
        ;;
    health)
        docker compose exec backend wget -qO- http://127.0.0.1:8080/health && echo ""
        ;;
    *)
        echo "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
