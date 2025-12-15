#!/usr/bin/env bash
# Installs Python dependencies from requirements.txt and checks for conflicts.

set -e

echo "====================================="
echo "Installing Python Requirements"
echo "====================================="

# Install dependencies from requirements.txt
python -m pip install -r requirements.txt

echo ""
echo "====================================="
echo "Checking for Dependency Conflicts"
echo "====================================="

# Use pip check to validate all dependencies are compatible
# This will fail if there are any conflicts
python -m pip check

echo ""
echo "====================================="
echo "Dependency Tree"
echo "====================================="

# Show dependency tree with warnings for any issues
python -m pipdeptree --warn fail

echo ""
echo "====================================="
echo "✓ All packages installed successfully!"
echo "✓ No dependency conflicts detected."
echo "====================================="
