#!/bin/bash

# Setwise VSCode Extension Installation Script

echo "🎯 Installing Setwise VSCode Extension..."

# Check if Node.js is installed
if ! command -v npm &> /dev/null; then
    echo "❌ Node.js and npm are required but not installed."
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

# Check if VSCode is installed
if ! command -v code &> /dev/null; then
    echo "❌ VSCode command 'code' not found in PATH."
    echo "Please install VSCode and ensure 'code' command is available."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Compile TypeScript
echo "🔨 Compiling TypeScript..."
npm run compile

# Package extension
echo "📦 Packaging extension..."
if ! command -v vsce &> /dev/null; then
    echo "Installing @vscode/vsce (Visual Studio Code Extension manager)..."
    npm install -g @vscode/vsce
fi

vsce package

# Install extension
echo "🚀 Installing extension in VSCode..."
VSIX_FILE=$(ls *.vsix | head -n 1)
if [ -f "$VSIX_FILE" ]; then
    code --install-extension "$VSIX_FILE"
    echo "✅ Setwise extension installed successfully!"
    echo "📝 Open a questions.py file to start using the extension."
else
    echo "❌ Failed to create extension package."
    exit 1
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Next steps:"
echo "1. Open VSCode"
echo "2. Create or open a questions.py file"
echo "3. Use snippets: type 'mcq' or 'subjective' and press Tab"
echo "4. Press Ctrl+Shift+P (Cmd+Shift+P) to preview quiz"
echo ""
echo "For help, see: https://github.com/nipunbatra/setwise"