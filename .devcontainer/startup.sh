#!/bin/bash
# Startup script for Codespaces
# This script is automatically executed when the devcontainer starts

set -e

echo "🚀 Starting YouTube Subtitles CLI..."
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "✓ Dependencies installed"
echo ""
echo "📝 Available commands:"
echo "  - CLI mode: python download_captions.py <url> [output_path] [language]"
echo "  - Web mode: python app.py"
echo "  - Or run: uvicorn app:app --host 0.0.0.0 --port 8000 --reload"
echo ""
echo "🌐 To start the web interface:"
echo "  python app.py"
echo ""
echo "✓ Setup complete! You can now use the YouTube Subtitles CLI"
