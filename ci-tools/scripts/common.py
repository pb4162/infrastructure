import os
import json
import subprocess

def get_changed_files():
    PIPELINE_FILES = os.getenv("CI_PIPELINE_FILES")
    if PIPELINE_FILES is not None:
        print("Getting changed files for pipeline")
        changed_files = json.loads(PIPELINE_FILES)
    else:
        print("Getting changed files for pipeline with >500 files touched")
        raise NotImplementedError("TODO: Get list of changed files when >500 files changed")
        # BEFORE_PUSH_COMMIT = os.getenv("CI_PREV_COMMIT_SHA")
        # AFTER_PUSH_COMMIT = os.getenv("CI_COMMIT_SHA")
        # diff_command = ["git", "diff", "--name-only", BEFORE_PUSH_COMMIT, AFTER_PUSH_COMMIT]
        # changed_files = subprocess.check_output(diff_command, text=True).split()
    return changed_files
