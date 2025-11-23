#!/usr/bin/env bash
set -euo pipefail

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI 'gh' is required. Install from https://cli.github.com/" >&2
  exit 1
fi

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <github-username-or-org> <repo-name>" >&2
  exit 1
fi

OWNER="$1"
REPO="$2"

# Initialize git repo if not already
if [ ! -d .git ]; then
  git init
fi

git add .
if ! git diff --cached --quiet; then
  git commit -m "Initial blog app scaffold"
fi

# Create GitHub repo if it doesn't exist
if ! gh repo view "$OWNER/$REPO" >/dev/null 2>&1; then
  gh repo create "$OWNER/$REPO" --public --source=. --remote=origin --push
else
  git remote add origin "git@github.com:$OWNER/$REPO.git" 2>/dev/null || true
  git push -u origin main || git push -u origin HEAD:main
fi
