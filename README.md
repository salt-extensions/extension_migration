# Salt Extension Migration

This repository is used to track and coordinate the migration of Salt modules to extensions.

## Getting Started

Follow these steps to set up your development environment and migrate Salt modules to extensions.

### 1. Install the salt-extension Tool

First, install the `salt-extension` tool by following the instructions in the [salt-extension
repository](https://github.com/saltstack/salt-extension).

### 2. Set Up Your Working Environment

Create an empty working directory and navigate into it:

```bash
mkdir working-dir
cd working-dir
```

### 3. Create a Directory for Extension Migration

Inside the working directory, create an empty directory to hold the extension migration files:

```bash
mkdir apache
cd apache
```

### 4. Create the New Salt Extension

Use the create-salt-extension command to create a new Salt extension inside the extension migration directory. Replace
the placeholders with your information:

```bash
create-salt-extension -A "Maintainer Name" \
    -E "maintainer@example.com" \
    -S "Salt Extension for interacting with Apache" \
    -U "https://github.com/salt-extensions/saltext-apache" \
    -L apache \
    --dest saltext-apache \
    apache
```

> **Note:** The `-L apache` option sets the license of the extension to "Apache 2.0" and should not be changed when
> replacing placeholder text in the previous command. The other `apache` will be replaced with the name of the extension you are migrating.

### 5. Set Up the Extension Repository

Navigate into the extension directory and initialize it as a Git repository:

```bash
cd saltext-apache
git init --initial-branch=main
pip install pre-commit
pre-commit install
git commit -a -m "Initial commit of extension framework"
```

> **Note:** In case of failures due to pinned project dependencies, clean out build and artifacts like below, and try again.

```bash
sudo rm -rf ./build/*
sudo rm -rf ./artifacts/*
git commit -a -m "Initial commit of extension framework"
```

## Migrating Salt Modules to Extensions

Follow these instructions to migrate Salt modules to extensions.

### 1. Dry Run Migration

First, git clone this extension-migration to your local environment into a separate folder not in your saltext-_____.

To perform a dry run migration of modules that contain "apache" in their name from a branch called "filter-source" into
an extension directory called "saltext-apache", use the following command:

```bash
extension-migrate.py --dry_run \
    --file_filter apache \
    --source_branch filter-source \
    --extension_dir saltext-apache
```

### 2. Actual Migration

To perform the actual migration of modules, use the following command:

```bash
extension-migrate.py --file_filter apache \
    --source_branch filter-source \
    --extension_dir saltext-apache
```

### 3. Conflict Resolution

If there are any merge conflicts, resolve them manually.

### 4. Merge Changes

Merge the "filter-target" branch into the main branch:

```bash
git commit -a -m "Merging in modules from Salt"
git checkout main
git merge filter-target
```

### 5. Code Refactoring

Change any references of `__utils__` to `salt.utils`:

```bash
SALTEXT_NAME=apache salt-rewrite -F fix_saltext_utils_imports .
```

### 6. Push Changes

Finally, push the changes to the Salt extension's repository. Contact an Owner of the `salt-extensions` organization to
obtain a repository for your Extension.
