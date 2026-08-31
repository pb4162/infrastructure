import os
import sys
import json
import subprocess
import textwrap
import requests


def run_site_playbook(*, tags=None, limits=None):
    if tags is None:
        tags = []
    if limits is None:
        limits = []
    payload = {
        "template_id": int(os.getenv("SEMAPHOREUI_TASK_TEMPLATE_ID")),
        "limit": ",".join(limits),
        "params": {
            "tags": tags
        }
    }
    headers = {
        "Authorization": f"Bearer {os.getenv('SEMAPHOREUI_KEY')}",
        "Content-Type": "application/json"
    }
    r = requests.post(
        f"{os.getenv('SEMAPHOREUI_HOST')}/api/project/{os.getenv('SEMAPHOREUI_PROJECT_ID')}/tasks",
        data=json.dumps(payload),
        headers=headers,
    )
    print("Sending payload:", payload)
    print(f"Got {r} from semaphoreui instance")


# TODO: pull these from env
BASE_DIR = "ansible"
SITE_PLAYBOOK = "playbooks/site.yml"

BEFORE_PUSH_COMMIT = os.getenv("CI_PREV_COMMIT_SHA")
AFTER_PUSH_COMMIT = os.getenv("CI_COMMIT_SHA")

diff_command = ["git", "diff", "--name-only"]
if BEFORE_PUSH_COMMIT == "0"*40:
    diff_command.append("HEAD~1")
else:
    diff_command.extend([BEFORE_PUSH_COMMIT, AFTER_PUSH_COMMIT])

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
