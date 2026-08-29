import os
import sys
import subprocess
import requests


def run_site_playbook(*, tags=None, limits=None):
    if tags is None:
        tags = []
    payload = {
        "template_id": int(os.getenv("SEMAPHOREUI_TASK_TEMPLATE_ID")),
        "limit": ",".join(limits),
        "params": {
            "tags": tags
        }
    }
    headers = {
        "Authorization": f"Bearer {os.getenv('SEMAPHOREUI_KEY')}"
    }
    requests.post(
        f"{os.getenv('SEMAPHOREUI_HOST')}/api/project/{os.getenv('SEMAPHOREUI_PROJECT_ID')}/tasks",
        data=payload,
        headers=headers,
    )


BASE_DIR = "ansible"
SITE_PLAYBOOK = "playbooks/site.yml"

parsed = {}

for arg in sys.argv[1:]:
    if "=" in arg:
        key, val = arg.split("=", 1)
        parsed[key] = val

BEFORE_PUSH_COMMIT = parsed.get("BEFORE_PUSH_COMMIT")
AFTER_PUSH_COMMIT = parsed.get("AFTER_PUSH_COMMIT")

diff_command = ["git", "diff", "--name-only", BEFORE_PUSH_COMMIT, AFTER_PUSH_COMMIT]
changed_files = subprocess.check_output(diff_command, text=True).split()

RUN_FULL_PLAYBOOK_PATHS = [
    f"{BASE_DIR}/{p}" for p in [
        SITE_PLAYBOOK,
        "ansible.cfg",
        "inventory.ini",
        "host_vars/all/all.yml"
        "group_vars/all/all.yml"
    ]
]

if any(p in changed_files for p in RUN_FULL_PLAYBOOK_PATHS):
    run_site_playbook()
    sys.exit(0)

tags = []

for path in changed_files:
    if path.startswith(f"{BASE_DIR}/roles/"):
        tags.append(path.split("/")[2])

limits = []

for path in changed_files:
    if path.startswith(f"{BASE_DIR}/group_vars/") or path.startswith(f"{BASE_DIR}/host_vars/"):
        path_split = path.split("/")
        limit = path_split[2]
        tag = path_split[3]
        # TODO: add support for .yaml?
        if tag.endswith(".yml"):
            tag = tag[:-4]
        if tag.endswith(".sops.yml"):
            tag = tag[:-9]
        tags.append(tag)
        limits.append(limit)

tags = list(set(tags))
limits = list(set(limits))

print("Got tags:", tags)
print("Got limits:", limits)

if len(tags) == 0 and len(limits) == 0:
    print("tags and limits lists empty, exiting")
    sys.exit(0)

run_site_playbook(tags=tags, limits=limits)
