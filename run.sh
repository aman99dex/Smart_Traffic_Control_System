#!/bin/bash

# Smart Traffic Control System - Quick Start Script
# This script sets up and runs the Smart Traffic Control System

set -e

echo "=========================================="
echo "Smart Traffic Control System - Setup"
echo "=========================================="

# Check Python version
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

python_version=$(python3 --version | awk '{print $2}')
echo "Found Python $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run tests
echo "Running system tests..."
python3 test_system.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "Setup Complete! Starting application..."
    echo "=========================================="
    python3 Main.py
else
    echo ""
    echo "Error: Tests failed. Please check the output above."
    exit 1
fi
