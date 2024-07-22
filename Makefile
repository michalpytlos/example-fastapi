.PHONY: up-setup build-test up-test flake8 isort black mypy lint bandit pip-audit

TEST_CONTAINER=postboard-api-test-1

down:
	docker compose -f docker-compose.yml -f docker-compose.api.yml down
up-setup:
	@if [ ! -f .env.test ]; then \
		cp .env.example .env.test && echo ".env.test file created"; \
	else \
		echo ".env.test already exists"; \
	fi

# tests
build-test:
	docker build --target test --tag postboard-api-test .
up-test: up-setup
	docker compose -f docker-compose.yml -f docker-compose.api.yml up -d test
test: up-test
	PYTEST_ARGS="--cov=app --cov-report=term-missing:skip-covered --cov-branch --cov-report=html:coverage_report"; \
	docker exec $(TEST_CONTAINER) pytest $$PYTEST_ARGS tests


# linting
flake8: up-test
	docker exec $(TEST_CONTAINER) flake8 app
isort: up-test
	docker exec $(TEST_CONTAINER) isort --check-only app
black: up-test
	docker exec $(TEST_CONTAINER) black --check app
mypy: up-test
	docker exec $(TEST_CONTAINER) mypy app
lint: flake8 isort black mypy

# security
bandit: up-test
	docker exec $(TEST_CONTAINER) bandit -r app
pip-audit: up-test
	docker exec $(TEST_CONTAINER) pip-audit || true
