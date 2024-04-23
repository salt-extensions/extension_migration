# Salt Extension Migration

This repository is used to track and coordinate the migration of Salt modules to extensions.

## Getting Started

Follow these steps to set up your development environment and migrate Salt modules to extensions.

### 1. Set Up Your Working Environment

Create an empty working directory and navigate into it:

```bash
mkdir working-dir
cd working-dir
```

### 2. Create a Directory for Extension Migration

Inside the working directory, create an empty directory to hold the extension migration files:

```bash
mkdir apache
cd apache
```

### 3. Create the New Salt Extension

Use the copier template for the latest framework of Salt Extensions. This is the preferred way to create a new extension,
as there is a lot of shared code between extensions that is easier to keep in sync with copier.

Install copier
```bash
pip install copier copier-templates-extensions
```

```bash
copier copy --trust https://github.com/salt-extensions/salt-extension-copier saltext-apache
```


### 4. Set Up the Extension Repository

Navigate into the extension directory:

```bash
cd saltext-apache
```

If you used the copier command to create the extension, it creates some boilerplate modules and tests
that we want to get rid of before we pull in the actual code from Salt.

```bash
find src tests -type f ! -name __init__.py ! -name conftest.py -delete
```

Initialize it as a Git repository:

```bash
git init --initial-branch=main
pip install pre-commit  # may not need to be done again if in a pre-existing virtual environment
pre-commit install
git add .
git commit -m "Initial commit of extension framework"
```
> *You may need to `pip install` `git-filter-repo` and `pylint`.
> If you are using git < 2.28, the `initial-branch` option is not present and `git init` will default to the branch being "master" instead of "main". Note that you won't be able to change it with `git branch -m master main` until after your first commit.

> **Note:** In case of failures due to pinned project dependencies, clean out build and artifacts like below, and try again.

```bash
sudo rm -rf ./build/*
sudo rm -rf ./artifacts/*
git add .
git commit -m "Initial commit of extension framework"
```

## Migrating Salt Modules to Extensions

Follow these instructions to migrate Salt modules to extensions.

### 1. Dry Run Migration

First, git clone this extension-migration to your local environment into a separate folder, not in your `saltext-_____` (if it isn't already).

then, cd into the directory before saltext-_______ (example, the `helm` directory instead of `saltext-helm`)

To perform a dry run migration of modules that contain "apache" in their name from a branch called "filter-source" into
an extension directory called "saltext-apache", use the following command:

```bash
extension-migrate.py --dry_run \
    --file_filter apache \
    --source_branch filter-source \
    --extension_dir saltext-apache
```

Note that all the dry-run does is preprare the command and then echo it to the terminal. If you run the dry run, and then the actual migration, you may get a `fatal error` complaining something already is created. This is not actaully a fatal error and can be safely ignored.

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
git add .
git commit -m "Merging in modules from Salt"
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
