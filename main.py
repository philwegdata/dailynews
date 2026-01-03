#!/usr/bin/env python3
"""
AI News Aggregator - Main Entry Point

This script starts the FastAPI server with the scheduler.
The scheduler will automatically fetch and aggregate news every day at 6 AM CET.
"""

import uvicorn
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))


def main():
    """Start the application server"""
    print("=" * 60)
    print("AI News Aggregator - Starting...")
    print("=" * 60)
    print()
    print("Server will start on: http://localhost:8000")
    print("Daily aggregation scheduled for: 6:00 AM CET")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()

    # Run the FastAPI application
    uvicorn.run(
        "backend.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )


if __name__ == "__main__":
    main()
