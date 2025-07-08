#!/bin/bash

set -euo pipefail

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*"
}

print_usage() {
  cat <<EOF
Usage: $SCRIPT_NAME [OPTIONS...]
Requirements helper script.

Options:
  --dev    	Installing dependencies for local running
  --qa         	Installing dependencies for automated testing
  --stage       Installing dependencies for staging environment
  --prod       	Requirements for production
  -h, --help    Call for help
EOF
}

install_local() {
  python3 -m venv venv
  source venv/bin/activate
  pip install uvicorn Django djangorestframework drf-spectacular django-debug-toolbar ipdb 
}

install_qa() {
  pip install Django djangorestframework drf-spectacular pytest pytest-django pytest-cov pytest-mock requests-mock django-mock-queries
}

install_stage() {
  pip install uvicorn Django djangorestframework psycopg2-binary drf-spectacular
}

install_prod() {
  pip install uvicorn Django djangorestframework psycopg2-binary redis django-cors-headers 
}

if [[ $# -eq 0 ]]; then
  print_usage
  exit 1
fi

for arg in "$@"; do
  case "$arg" in
    --local)
      install_local
      ;;
    --qa)
      install_qa
      ;;
    --stage)
      install_stage
      ;;
    --prod)
      install_prod
      ;;
    -h|--help)
      print_usage
      exit 0
      ;;
    *)
      echo "Error: Unknown option '$arg'" >&2
      print_usage
      exit 1
      ;;
  esac
done

