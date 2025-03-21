# Daily Automations for IT Professionals

A repository with examples and slides for showing off simple daily automations for IT professionals. 

## Slides and script

Check out the slides at https://noahlehmann.github.io/talk-daily-automations/slides.pdf!

## Setup

### Git hooks

Install the git hooks by running the following command ...

```bash
make git
```

... or by manually placing the contents of the `.githooks` directory in your `.git/hooks` directory.

#### GitGuardian

[GitGuardian's `ggshield`](https://github.com/GitGuardian/ggshield) helps you to prevent secrets from being committed to your repository.
This is achieved via a pre-commit hook that scans your changes for secrets.

For the pre-commit hook to work, you need to provide a GitGuardian API key.
This can be automatically done via browser if you simply authenticate via:

```bash
ggshield auth login
```

This is assuming you have a free account at GitGuardian - if not, just set one up.

Now `ggshield` will automatically scan your changes for secrets before you commit them and fail the commit if it finds 
anything, preventing the secrets to be published in the repository.

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
