#!/usr/bin/env bash

# Script args
PYTEST_ARGS=""
TESTS_TO_EXECUTE="tests"
while getopts ":chf:" opt; do
    case $opt in
        c)
            PYTEST_ARGS="--cov=app --cov-report=term-missing:skip-covered --cov-branch --cov-report=html"
            ;;
        f)  
            TESTS_TO_EXECUTE="tests/${OPTARG}"
            ;;
        h)
            echo "Usage: test.sh [-c] [-f <file>]"
            echo "  -c: Run tests with coverage"
            echo "  -f <file>[::<test>]: Run specified tests only"
            echo "  -h: Show this help message"
            exit 0
            ;;
        \?)
            echo "Invalid option: -$OPTARG"
            exit 1
            ;;
    esac
done

# Cleanup if containers are started by this script
top_output=$(docker compose top)

cleanup() {
    if [ -z "$top_output" ]; then 
        docker compose down
    fi
}

trap cleanup EXIT

# Run db
docker compose up -d postgres
until pg_isready -h localhost -p 5432; do sleep 1; done;

# Load env vars
while read -r line; do
    export "$(echo $line)"
done < .env.local

# Activate venv
source $(poetry env info --path)/bin/activate

# Run tests
COMMAND="pytest $PYTEST_ARGS -s -vv $TESTS_TO_EXECUTE"
echo $COMMAND
eval $COMMAND
