# Infrastructure

This repository contains everything used to manage my infrastructure, including but not limited to virtual machines, bare metal OS installations and cloud servers.

# Components

- **FluxCD** - Keeps the resources on my main kubernetes cluster up-to-date with the state of this repository
- **Ansible** - Used to configure OS installs in a way that is idempotent, meaning that running a playbook multiple times will still lead to the same final state. In practice this also means that changes are only made when needed.
- **Renovate** - Keeps applications up-to-date by scanning the repository and opening pull requests

# Equipment

- **Mini PC** (x3) - Main kubernetes nodes
- **Router** (x1) - Primary router/firewall
- **Home Server** (x1) - Primary NAS for bulk storage and miscellaneous workloads
- **Raspberry Pi** (x1) - Runs Semaphore UI (to manage ansible playbooks), Technitium (for DNS) and miscellaneous workloads

# External Dependencies

While I aim to be reliant on as few external services as possible, there are still a few that I use:

- **Cloudflare** - External DNS
- **LetsEncrypt** - SSL/TLS certificates
- **Hetzner** - Two separate VPSes are used: one for Headscale and one as a jump host for public facing services
- **GitHub** - Hosts this repository
- **Telegram** - Alertmanager and Gatus notifications

# Provisioning

## Initial Setup

- Adjust BIOS settings to lower power limits and turn on `Wake on AC Power Loss`
- Setup machines with the following OSes:
  - `Router` - Vanilla OpenWRT
  - `Mini PCs` - Debian
  - `Raspberry Pi` - Raspberry Pi OS
  - `Home Server` - Proxmox. TrueNAS and Debian are then installed into separate VMs.
- Enable SSH and a separate user account in the OS install
- Upload SSH keys
- Assign static IPs

**Helpful links for setting up OpenWRT:**
- https://openwrt.org/toh/gl.inet/gl-mt6000
- https://openwrt.org/docs/guide-quick-start/walkthrough_login

## Configuration

Before running Ansible first check over group and host vars and populate any fields that are missing or outdated.

OS provisioning is done in 2 stages. To apply the first stage:
```ansible-playbook -Kk playbooks/[site]/[playbook].yml -t bootstrap -i [path to inventory] --diff```

For subsequent runs Semaphore UI is used. The command-line equivalent would be:
```ansible-playbook -K playbooks/[site]/[playbook].yml -i [path to inventory] --diff```

## Post Provisioning

- For new machines that are Tailscale subnet routers or exit nodes, enable their routes in Headscale
- Tag disks in Longhorn with the `ssd` tag

# Credits

- https://rpi4cluster.com
- https://github.com/geerlingguy/internet-pi
- https://github.com/geerlingguy/pi-cluster
