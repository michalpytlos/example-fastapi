set -e
set -x

# Activate venv
source $(poetry env info --path)/bin/activate

# Security
bandit -r app
# Only fail pip-audit if vulnerabilities are fixable
test -z "$(pip-audit --format=json 2>/dev/null | jq '.dependencies[].vulns[].fix_versions[]')" || pip-audit

# Linting
flake8 app
black app --check
isort app --profile black --check-only

# Static type checking
mypy app
