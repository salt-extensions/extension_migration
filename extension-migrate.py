#!/usr/bin/env python

import argparse
import fnmatch
import os
import re
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--source_branch", help = "Source Branch.", required=True)
parser.add_argument("-f", "--file_filter", help = "Name to use to filter files, also name of the extension.", required=True)
parser.add_argument("-n", "--dry_run", help = "Dry run.", action="store_true")
parser.add_argument("-e", "--extra_files", nargs="+", help = "Exta files.", required=False)
parser.add_argument("-d", "--extension_dir", help = "Extension directory.", required=True)

args = parser.parse_args()

# Clone salt
print("Cloning Salt")
previous_cwd = os.getcwd()
cmd = ["git", "clone", "git@github.com:saltstack/salt.git", "--single-branch"]
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
os.chdir("salt")

# Create the filter-source branch
print("Checking out filter-source branch")
cmd = ["git", "checkout", "-b", "filter-source"]
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()

print("Calculating files")
files_to_migrate = []
for root, dirs, files in os.walk("."):
    path = root.split(os.sep)
    for _file in fnmatch.filter(files, f"*{args.file_filter}*"):
        full_path = "/".join(path)
        dirname_full_path_file = os.path.dirname(f"{full_path}/{_file}")
        files_to_migrate.append(f"{full_path}/{_file}")
        if os.path.exists(f"{dirname_full_path_file}/conftest.py"):
            files_to_migrate.append(f"{dirname_full_path_file}/conftest.py")
        if os.path.exists(f"{dirname_full_path_file}/__init__.py"):
            files_to_migrate.append(f"{dirname_full_path_file}/__init__.py")
        parent_dirname_full_path_file = os.path.dirname(f"{dirname_full_path_file}")
        if os.path.exists(f"{parent_dirname_full_path_file}/__init__.py"):
            files_to_migrate.append(f"{parent_dirname_full_path_file}/__init__.py")

    for _dir in fnmatch.filter(dirs, f"*{args.file_filter}*"):
        full_path = "/".join(path)
        files_to_migrate.append(f"{full_path}/{_dir}")

    for _file in fnmatch.filter(files, "*conftest.py*"):
        full_path = "/".join(path)
        file_full_path = f"{full_path}/{_file}"
        if file_full_path in ("./tests/pytests/unit/conftest.py",
                              "./tests/pytests/integration/conftest.py",
                              "./tests/pytests/functional/conftest.py"):
            files_to_migrate.append(f"{full_path}/{_file}")

# Add any extra files
if args.extra_files:
    for extra_file in args.extra_files:
        if os.path.exists(extra_file):
            files_to_migrate.append(extra_file)
        else:
            print(f"{extra_file} does not exist, skipping")

old_files = []
new_files = []

for file in files_to_migrate:

    new_file = re.sub("\.\/", "", file)
    old_files.append(new_file)

    # swap doc for docs
    new_file = re.sub("^doc", "docs", new_file)

    # swap salt path for extension path
    new_file = re.sub("^salt", f"src/saltext/saltext_{args.file_filter}", new_file)

    new_files.append(new_file)

print("Filtering files")
cmd = ["git", "filter-repo"]
for count in range(len(old_files)):
    cmd.append("--path")
    cmd.append(f"{old_files[count]}")
cmd.append("--refs")
cmd.append("refs/heads/filter-source")
cmd.append("--force")

if args.dry_run:
    print(" ".join(cmd))
else:
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

print("")

print("Renaming Paths")
cmd = ["git", "filter-repo"]
for count in range(len(old_files)):
    cmd.append("--path-rename")
    cmd.append(f"{old_files[count]}:{new_files[count]}")
cmd.append("--force")

if args.dry_run:
    print(" ".join(cmd))
else:
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

os.chdir(previous_cwd)

# change into extension directory
os.chdir(args.extension_dir)

# Create the filter-target branch
print("Checking out filter-target branch")
cmd = ["git", "checkout", "-b", "filter-target"]
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()

print("Adding repo-source remote")
cmd = ["git", "remote", "add", "repo-source", "../salt"]
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()

print("Fetch repo-source remote")
cmd = ["git", "fetch", "repo-source"]
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()

print("Creating the branch-source branch")
cmd = ["git", "branch", "branch-source", "remotes/repo-source/filter-source"]
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()

print("Merge branch-source into extension")
cmd = ["git", "merge", "branch-source", "--allow-unrelated-histories"]
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
