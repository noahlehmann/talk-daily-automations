# Daily Automations for IT Professionals

A repository with examples and slides for showing off simple daily automations for IT professionals. 

## Slides and script

Check out the slides at https://noahlehmann.github.io/talk-daily-automations/slides.pdf!

### Prerequisites

- Python (used 3.13)
- Node.js (used 20)
- Make (used 3.81)
- Git (used 2.48)

## Setup

### Git hooks

Install the git hooks by running the following command ...

```bash
make git
```

... or by manually placing the contents of the `.githooks` directory in your `.git/hooks` directory.

#### GitGuardian

[GitGuardian's `ggshield`](https://github.com/GitGuardian/ggshield) helps you to prevent secrets from being committed to your repository.
This is achieved via a pre-commit hook that scans your changes for secrets. Follow [the Github instructions](https://github.com/GitGuardian/ggshield?tab=readme-ov-file#installation) to install `ggshield`.

For the pre-commit hook to work, you need to provide a GitGuardian API key.
This can be automatically done via browser if you simply authenticate via:

```bash
ggshield auth login
```

This is assuming you have a free account at GitGuardian - if not, just set one up.
Now `ggshield` will automatically scan your changes for secrets before you commit them and fail the commit if it finds 
anything, preventing the secrets to be published in the repository.

### Init the project environment

Simply run the following command ...

```bash
make init
```

This will do a few tasks for you that would usually be done manually:

#### Create a Python virtual environment
```bash
python3 -m venv .venv
```

#### Install the Python requirements
```bash
pip install -r infrastructure/ansible/requirements.txt -r src/api/requirements.txt
```
 
#### Init the node modules
```bash
cd src/web && npm install
```

#### Initialize the SQLite database for the API
```bash
source .venv/bin/activate
cd src/api && flask db upgrade
```

## Run the project

After initialization you can run the components in standalone mode.

### Static webpage

The webpage is statically linked and only uses NodeJS to minify and lint the scripts.
Simply open the `index.html` file in your browser.
The page will need the API to be online to work properly.

### Python API + Database

```bash
source .venv/bin/activate
cd src/api && flask run
```

If you already have a database in the `src/api/instances` directory, you might need to run the migration scripts on it if any were added.

```bash
cd src/api && flask db upgrade
```

### Use compose

You can also use `docker-compose` to run the API and the database in a more production like environment.

```bash
docker compose up -d --build
```

This will expose the webpage on http://localhost:80.

Simply stop it by running `docker compose down -v`. 
The `-v` option will remove all volumes and therefore reset the database.

### Use make

If this is still too much to remember, just run:

```bash
make run-local
```

Just remember this starts the compose in the background, remember to stop it.

## Devcontainer





## Deployment

### Helm

Test the install of your Helm chart by running ...

```bash
touch ./kubeconfig
helm dependency update ./chart/counter
```

And then running ...

```bash
helm upgrade --install \
  --kubeconfig ./kubeconfig \
  --namespace fgils-1 \
  counter-example ./chart/counter \
  --set postgres.auth.password="replaceme" # replace
```
