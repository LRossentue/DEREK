#!/bin/bash
# Setup script for Ollama and llama3.2:3b model
# Run this to get Derek MCP ready for LLM mode

set -e  # Exit on error

echo "=========================================="
echo "Derek MCP - Ollama Setup Script"
echo "=========================================="
echo ""

# Check if Ollama is already installed
if command -v ollama &> /dev/null; then
    echo "✓ Ollama is already installed at: $(which ollama)"
    echo ""
else
    echo "Installing Ollama..."
    echo ""
    curl -fsSL https://ollama.com/install.sh | sh
    echo ""
    echo "✓ Ollama installed successfully"
    echo ""
fi

# Check if Ollama service is running
echo "Checking Ollama service..."
if pgrep -x "ollama" > /dev/null; then
    echo "✓ Ollama service is already running"
else
    echo "Starting Ollama service..."
    ollama serve > /tmp/ollama.log 2>&1 &
    sleep 3
    echo "✓ Ollama service started"
fi
echo ""

# Pull the model
echo "Pulling llama3.2:3b model (~2GB download)..."
echo "This may take a few minutes depending on your connection..."
echo ""
ollama pull llama3.2:3b
echo ""
echo "✓ Model downloaded successfully"
echo ""

# Test the model
echo "Testing model with a quick query..."
echo ""
TEST_RESPONSE=$(ollama run llama3.2:3b "Say 'Derek is ready' in exactly three words" --verbose=false 2>&1 | head -n 1)
echo "Model response: $TEST_RESPONSE"
echo ""

# Test API endpoint
echo "Testing Ollama API endpoint..."
API_TEST=$(curl -s http://localhost:11434/api/tags)
if [ $? -eq 0 ]; then
    echo "✓ Ollama API is responsive"
else
    echo "✗ Warning: Ollama API may not be responding correctly"
fi
echo ""

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Ollama is ready for Derek MCP."
echo "Model: llama3.2:3b"
echo "API: http://localhost:11434"
echo ""
echo "Next steps:"
echo "  1. Install Derek MCP: pip install -e ."
echo "  2. Run Derek: derek_mcp"
echo ""
echo "To check Ollama status later:"
echo "  ollama list              # Show installed models"
echo "  ollama ps                # Show running models"
echo "  curl http://localhost:11434/api/tags  # Test API"
echo ""
