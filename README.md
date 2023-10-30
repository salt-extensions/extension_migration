A repository to track and coordinate the migration of Salt modules to extensions.

### Install the salt-extension tool
https://github.com/saltstack/salt-extension

### Instructions for running extension-migrate.py

Dry run migration of modules that contain "apache" in their name from a branch called "filter_source into an extension directory called "saltext-apache"
```
extension-migrate.py --dry-run --file_filter apache --source_branch filter-source --extension_dir saltext-apache
```

Migration of modules that contain "zookeeper" in their name from a branch called "filter_source into an extension directory called "saltext-zookeeper"
```
extension-migrate.py --file_filter zookeeper --source_branch filter-source --extension_dir saltext-zookeeper
```
