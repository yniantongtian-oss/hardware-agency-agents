#!/usr/bin/env bash
# Export this checkout's hardware agents to a host format.
# Does not clone a remote and does not write outside --dest.
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$root/scripts/export_agents.py" "$@"
