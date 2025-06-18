#!/bin/bash
#
# Install git hooks for the project
# Run this script after cloning the repository
#

set -e

echo "📦 Installing git hooks..."

# Create hooks directory if it doesn't exist
mkdir -p .git/hooks

# Copy pre-push hook
cp scripts/pre-push .git/hooks/pre-push
chmod +x .git/hooks/pre-push

echo "✅ Git hooks installed successfully!"
echo "💡 The pre-push hook will now run tests before each push."
echo "   If tests fail, the push will be blocked."