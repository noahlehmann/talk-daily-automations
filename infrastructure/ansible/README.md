# Ansible

This playbook collection is an example of how to deploy prometheus and grafana with ansible.

## Setup

```bash
touch ~/.env/vaultpass
```

```bash
pip install -r requirements.txt
```

## Run

```bash
ansible-playbook \
  --private-key=./.env/ssh_key \
  --vault-password-file=./.env/vaultpass \
  playbooks/create_lxc.yaml
```