# Example API built with FastAPI

The implementation loosely follows the [fastapi-course](https://github.com/Sanjeev-Thiyagarajan/fastapi-course) app

## Setup

### Initial local setup
App runs locally, database runs in a container.

1. Install the required Python version: `pyenv install 3.11`
1. Create the env: `pyenv shell 3.11 && pyenv which python | xargs poetry env use`
1. Install the project dependencies: `poetry install`
1. Install `pg_isready`: `sudo apt install postgresql-client`
1. Create .env.local file: `make local-setup`

### Running test
* Run from command line: `bash test.sh -h`
* or use VS Code - see the configuration in `.vscode/settings.json`

### Running app
* Run using docker: `make up`
* or use VS Code - see the configuration in `.vscode/launch.json`
