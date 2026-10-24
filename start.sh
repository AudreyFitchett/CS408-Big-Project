#!/usr/bin/env bash
#
# Start the todo app on your own machine.
#
# Checks that everything the app needs is in place before starting it, so a
# missing tool or a skipped install gives you a sentence to read instead of a
# stack trace.
#
#   ./start.sh              start the app on http://localhost:3000
#   ./start.sh --dev        restart automatically when you save a file
#   ./start.sh --port 4000  listen somewhere other than port 3000
#   ./start.sh --help       show this message
#
# This is for development. On a server, systemd starts the app instead --
# see deploy/setup-ec2.sh and deploy/todo-app.service.
#
# Works on macOS and Linux.

# Bash "strict mode": stop on the first error (-e), stop on an undefined
# variable (-u), and let a failure anywhere in a pipeline fail the whole
# pipeline (-o pipefail). Without these, a script keeps going after a step
# fails and leaves you guessing about what went wrong.
set -euo pipefail

# The package.json "engines" field asks for this too. Keep the two in step.
REQUIRED_PYTHON_VERSION=3

DEV_MODE="false"
PORT_OVERRIDE=""
APP_HOST="${APP_HOST:-127.0.0.1}"
APP_PORT="${APP_PORT:-8000}"

# --- helpers ----------------------------------------------------------------

say() {
    printf '==> %s\n' "$1"
}

die() {
    printf 'ERROR: %s\n' "$1" >&2
    exit 1
}

usage() {
    # Print this file's own comment block as the help text, so the help and the
    # documentation can never drift apart.
    awk 'NR>1 { if (/^#/) { sub(/^# ?/, ""); print } else { exit } }' "$0"
    exit 0
}

# --- options ----------------------------------------------------------------

# getopts (the shell builtin) only handles single-letter flags, so the long
# options are parsed by hand. Do NOT reach for the `getopt` command instead:
# macOS ships an old BSD version that does not support them either.
while [ $# -gt 0 ]; do
    case "$1" in
        -d|--dev)
            DEV_MODE="true"
            shift
            ;;
        -p|--port)
            [ $# -ge 2 ] || die "--port needs a number, for example: --port 4000"
            # Check it here, before the script does any real work. Failing on
            # bad input after a two-minute npm install is just rude.
            case "$2" in
                ''|*[!0-9]*) die "--port needs a number, got '$2'" ;;
            esac
            PORT_OVERRIDE="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            die "unknown option '$1' (try --help)"
            ;;
    esac
done

# Run from the project root no matter where this script was called from.
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

# --- checks -----------------------------------------------------------------

command -v python3 >/dev/null 2>&1 \
    || die "Python is not installed. Get it from https://www.python.org/downloads/release/python-3150/ (version ${REQUIRED_PYTHON_VERSION} or newer)."

# Let python compare its own version rather than parsing version strings in bash.
if ! python3 --version >= ${REQUIRED_PYTHON_VERSION}; then
    die "$(python3 --version) is too old. This app needs version ${REQUIRED_PYTHON_VERSION} or newer."
fi

#okay, the internet experts say it's a good idea to use a virtual environmnet, so I'm going to try that

#not sure this is going to work the way I intend but idk
python3 -m pip --version || die "pip is not installed, but Python is. Run the command python3 -m ensurepip --upgrade"

#python3 -c "import django" || die "django is not installed, but Python is. Run the command python3 -m pip install django"

#[ -f manage.py ] || { echo "ERROR: no manage.py found in $PROJECT_DIR" >&2; exit 1; }
[ -d "./venv" ] || { python3 -m venv venv; }


# Install dependencies on the first run, and again when they change (which is
# what happens right after a git pull).
#
# The marker to compare against is node_modules/.package-lock.json, which npm
# writes at the end of every install. Comparing against the node_modules
# directory itself does not work: npm often leaves its timestamp alone, so the
# check would fire on every single run.
INSTALL_MARKER=old_requirements.txt
REQUIREMENTS_FILE="requirements.txt"

[ -f "$REQUIREMENTS_FILE" ] || die "ERROR: $REQUIREMENTS_FILE not found."

# if [ ! -f requirements.txt ]; then
#     say "Installing dependencies (this happens once, and takes a moment)"
#     i=0
#     while IFS= read -r line; do
#         ./venv/bin/pip install $line;
#     done < requirements.txt
        #let's give this a try. The other option is to read the file, put it into an array, and then read the array smh
        #i=0;
        #while IFS= read -r line; do
        #    pydep[i]+="Item_$line"
        #     i++;
        # done <<< "$(cat requirements.txt)"
        # for item in "${pydep[@]}"; 
        #     do echo "$item"; 
        # done
if [ ! -f "$INSTALL_MARKER" ] || [ requirements.txt -nt "$INSTALL_MARKER" ]; then
    say "Dependencies changed since your last install, updating them"
    cp requirements.txt old_requirements.txt

    while IFS= read -r line; do
        ./venv/bin/pip install $line;
    done < requirements.txt
fi

# --- start ------------------------------------------------------------------

# PORT is read by server/server.js. Exporting it here is the same mechanism
# systemd uses on the EC2 server, just with a different value.
if [ -n "$PORT_OVERRIDE" ]; then
    export PORT="$PORT_OVERRIDE"
fi

PORT_IN_USE="${PORT_OVERRIDE:-3000}"
say "Starting on http://localhost:${PORT_IN_USE} -- press Ctrl+C to stop"

if [ "$DEV_MODE" = "true" ]; then
    say "Dev mode: Django runserver automatically restarts when you save a file"
    # exec replaces this shell with node, so Ctrl+C reaches node directly
    # instead of killing this wrapper and orphaning the server.
    exec python manage.py runserver "${PORT_IN_USE}"

else   
    say "Production mode: running with Gunicorn"
    exec ./venv/bin/gunicorn --bind "${APP_HOST}:$APP_PORT" lazygirl.wsgi:application
fi