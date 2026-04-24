#!/bin/bash
# launch.command - Campus IT Help Desk launcher
#
# How to run:
#   - Easiest: double-click HelpDesk.app in this folder.
#   - Or: double-click launch.command directly.
#
# FIRST-TIME SETUP on a fresh clone (one-liner from Terminal):
#   cd "$HOME/Desktop/it_help_desk" && chmod +x launch.command && xattr -cr launch.command 2>/dev/null; open launch.command
#
# What this script does:
#   1. Clears macOS quarantine on project files.
#   2. Sources .env if present (optional - just for SECRET_KEY).
#   3. Creates venv/, installs deps from requirements.txt.
#   4. Runs `flask init-db` (creates helpdesk.db on first run).
#   5. Starts the Flask app and opens http://127.0.0.1:5000.
#
# Database:
#   Defaults to SQLite (helpdesk.db, created automatically). No external DB
#   install needed. To use Postgres instead, set DATABASE_URL in .env.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

echo "=========================================="
echo "  Campus IT Help Desk - Launcher"
echo "=========================================="
echo ""

# -- Clear macOS quarantine (harmless if nothing to clear).
xattr -cr . 2>/dev/null || true

# -- Make sure the script is still executable.
chmod +x "$0" 2>/dev/null || true

# -- Load .env if present (optional).
if [ -f ".env" ]; then
    set -a
    # shellcheck disable=SC1091
    source ./.env
    set +a
fi
: "${SECRET_KEY:=local-test-secret}"
export SECRET_KEY
# DATABASE_URL is passed through only if set; otherwise the app uses SQLite.
[ -n "${DATABASE_URL:-}" ] && export DATABASE_URL

# -- Check: python3 --
if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: python3 is not installed or not on PATH."
    echo "Install it from https://www.python.org/downloads/  or  brew install python"
    echo ""
    echo "Press Enter to close this window."
    read -r
    exit 1
fi

# -- Create venv if missing --
if [ ! -d "venv" ]; then
    echo "Creating virtual environment (venv/)..."
    python3 -m venv venv || { echo "ERROR: failed to create venv."; read -r; exit 1; }
    echo ""
fi

# -- Activate venv --
# shellcheck disable=SC1091
source venv/bin/activate

# -- Install / update dependencies --
echo "Installing / updating dependencies..."
pip install --quiet --upgrade pip
if ! pip install --quiet -r requirements.txt; then
    echo "ERROR: pip install failed."
    echo "Press Enter to close this window."
    read -r
    exit 1
fi
echo "Dependencies ready."
echo ""

# -- Initialize database (idempotent; creates helpdesk.db on first run).
echo "Initializing database..."
if ! flask --app run.py init-db; then
    echo ""
    echo "ERROR: 'flask init-db' failed. Scroll up for the Python traceback."
    echo ""
    echo "Press Enter to close this window."
    read -r
    exit 1
fi
echo ""

# -- Open browser after a short delay.
( sleep 2 && open "http://127.0.0.1:5000" ) &

# -- Launch the app.
echo "=========================================="
echo "  Starting app on http://127.0.0.1:5000"
echo "  Press Ctrl+C in this window to stop."
echo "=========================================="
echo ""
python3 run.py

echo ""
echo "App stopped. Press Enter to close this window."
read -r
