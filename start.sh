#!/bin/bash

# AI News Aggregator - Start Script

echo "======================================================================"
echo "  AI News Aggregator"
echo "======================================================================"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run: python3 -m venv .venv"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  Warning: .env file not found!"
    echo "   AI summaries will not work without Google Gemini API key."
    echo "   To enable summaries:"
    echo "   1. Copy .env.example to .env"
    echo "   2. Get API key from: https://aistudio.google.com/apikey"
    echo "   3. Add key to .env file"
    echo ""
    read -p "Continue without API key? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "Starting AI News Aggregator..."
echo "Server will be available at: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop"
echo "======================================================================"
echo ""

# Start the application
python main.py
