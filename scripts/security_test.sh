#!/bin/bash
# Local security testing script for Setwise
# Run this script to perform comprehensive security checks

set -e

echo "🛡️  Setwise Security Testing"
echo "================================"

# Check if security tools are installed
echo "📋 Checking security tools..."

if ! command -v bandit &> /dev/null; then
    echo "❌ Bandit not found. Installing..."
    pip install bandit
fi

if ! command -v safety &> /dev/null; then
    echo "❌ Safety not found. Installing..."
    pip install safety
fi

if ! command -v pip-audit &> /dev/null; then
    echo "❌ pip-audit not found. Installing..."
    pip install pip-audit
fi

echo "✅ Security tools ready"
echo

# Run Bandit security scan
echo "🔍 Running Bandit security scan..."
echo "================================="
bandit -r . -f txt --skip B101,B404,B603,B607,B311 || true
echo

# Run Safety vulnerability check  
echo "🔍 Running Safety vulnerability check..."
echo "======================================="
safety check --ignore 77148 --ignore 77146 --ignore 77711 --ignore 77697 --ignore 76916 --ignore 77064 --ignore 65189 --ignore 77740 --ignore 77695 --ignore 72086 --ignore 76903 || true
echo

# Run pip-audit for dependency vulnerabilities
echo "🔍 Running pip-audit dependency scan..."
echo "======================================"
pip-audit --desc || true
echo

# Run tests with coverage
echo "🧪 Running tests with coverage..."
echo "================================"
python -m pytest -v --cov=. --cov-report=term-missing --cov-report=html || true
echo

echo "✅ Security testing completed!"
echo "📊 Check htmlcov/index.html for detailed coverage report"