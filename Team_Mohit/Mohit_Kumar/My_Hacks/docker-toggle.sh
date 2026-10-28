#!/bin/bash

case "$1" in
    start)
        echo "Starting Docker service..."
        sudo systemctl start docker
        echo "Docker started."
        ;;
    stop)
        echo "Stopping Docker service and socket..."
        sudo systemctl stop docker docker.socket
        echo "Docker stopped."
        ;;
    status)
        systemctl status docker --no-pager
        ;;
    *)
        echo "Usage: $0 {start|stop|status}"
        exit 1
        ;;
esac
