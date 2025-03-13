# Daily Automations for IT Professionals

A repository with examples and slides for showing off simple daily automations for IT professionals. 

## Setup

### Git hooks

Install the git hooks by running the following command ...:

```bash
./install_hooks.sh
```

... or by manually placing the contents of the `.githooks` directory in your `.git/hooks` directory.

#### GitGuardian

[GitGuardian](https://github.com/GitGuardian/ggshield) helps you to prevent secrets from being committed to your repository.
This is achieved via a pre-commit hook that scans your changes for secrets.

For the pre-commit hook to work, you need to provide a GitGuardian API key.
This can be automatically done via browser if you simply authenticate via:

```bash
ggshield auth login
```

This is assuming you have a free account at GitGuardian - if not, just set one up.