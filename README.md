A repository to track and coordinate the migration of Salt modules to extensions.

### Install the salt-extension tool
https://github.com/saltstack/salt-extension

Create an empty working directory
```
mkdir working-dir
```

Change into the working directory
```
cd working-dir
```

Create an empty directory to hold the extension migration files
```
mkdir apache
```

Change into the extension migration directory
```
cd apache
```

Create the new salt extension inside the extension migration directory
```
create-salt-extension -A "Maintainer Name" -E "maintainer@example.com" -S "Salt Extension for interacting with Apache" -U "https://github.com/salt-extensions/saltext-apache" -L apache --dest saltext-apache saltext-apache
```

Setup the extension as a git repostitory
```
cd saltext-apache
git init .
pre-commit install
git add .
git commit -a
```
Previous commands will likely fail becuse project dependencies are being pinned.
Clean out build and artifacts and run away.
```
sudo rm -rf ./build/*
sudo rm -rf ./artifacts/*
git add .
git commit -a -m 'Initial extension layout'
```

### Instructions for running extension-migrate.py

Dry run migration of modules that contain "apache" in their name from a branch called "filter_source into an extension directory called "saltext-apache"
```
extension-migrate.py --dry_run --file_filter apache --source_branch filter-source --extension_dir saltext-apache
```

Migration of modules that contain "apache" in their name from a branch called "filter_source into an extension directory called "saltext-apache"
```
extension-migrate.py --file_filter apache --source_branch filter-source --extension_dir saltext-apache
```
