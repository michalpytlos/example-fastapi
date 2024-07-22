# Example API built with FastAPI

Simple RESTful post board API with JWT auth.

## Setup

### Initial local setup
App runs locally, database runs in a container.

1. Install required Python version: `pyenv install 3.11`
1. Create virtual env: `pyenv shell 3.11 && pyenv which python | xargs poetry env use`
1. Install project dependencies: `poetry install`
1. Install `pg_isready`: `sudo apt install postgresql-client`
1. Create `.env.local` file: `make local-setup`

### Running tests
* In Docker: `make test`
* Locally: `bash test.sh -h`
* Locally in VS Code (`.vscode/settings.json`)

### Running app
* In Docker: `make up`
* Locally in VS Code (`.vscode/launch.json`)

## Credits
The initial implementation of the project loosely followed the [Python API Development course](https://www.youtube.com/watch?v=0sOvCWFmrtA) from freeCodeCamp.
