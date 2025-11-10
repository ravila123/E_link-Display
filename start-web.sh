#!/bin/bash

# Start Web Interface for E-Paper Display
# Usage: ./start-web.sh

echo "=========================================="
echo "  E-Paper Display Web Interface"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Run: python3 -m venv .venv"
    echo "   Then: .venv/bin/pip3 install -r requirements.txt"
    exit 1
fi

# Check if Flask is installed
if ! .venv/bin/python3 -c "import flask" 2>/dev/null; then
    echo "📦 Installing web interface dependencies..."
    .venv/bin/pip3 install -r requirements-web.txt
fi

# Get Pi's IP address
IP_ADDRESS=$(hostname -I | awk '{print $1}')

echo "✅ Starting web interface..."
echo ""
echo "Access the interface at:"
echo "  • http://localhost:5000"
echo "  • http://raspberrypi.local:5000"
echo "  • http://$IP_ADDRESS:5000"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start the web interface
.venv/bin/python3 web_interface.py
