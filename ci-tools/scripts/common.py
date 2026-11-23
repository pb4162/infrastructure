import os
import json
import subprocess

def get_changed_files():
    PIPELINE_RERUNS = os.getenv("CI_PIPELINE_RERUNS")
    if PIPELINE_RERUNS is not None:
        print("Getting changed files for restarted pipeline")
        changed_files = json.loads(os.getenv("CI_PIPELINE_FILES"))
    else:
        print("Getting changed files for regular pipeline")
        BEFORE_PUSH_COMMIT = os.getenv("CI_PREV_COMMIT_SHA")
        AFTER_PUSH_COMMIT = os.getenv("CI_COMMIT_SHA")
        diff_command = ["git", "diff", "--name-only", BEFORE_PUSH_COMMIT, AFTER_PUSH_COMMIT]
        changed_files = subprocess.check_output(diff_command, text=True).split()
    return changed_files
