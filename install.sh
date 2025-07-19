#!/bin/bash

echo "🔧 ShadowWatch Auto Installer"
echo "-----------------------------"

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Install pip requirements
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Install Nmap
echo "🛰 Installing Nmap..."
sudo apt update
sudo apt install -y nmap

# Install Sherlock requirements
if [ -d "sherlock" ]; then
    echo "🕵️ Setting up Sherlock..."
    cd sherlock
    pip3 install -r requirements.txt
    cd ..
fi

# Done
echo "✅ Installation complete!"
echo "🚀 Launching ShadowWatch..."
python3 shadowwatch.py
