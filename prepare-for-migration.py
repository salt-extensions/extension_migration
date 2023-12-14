import os
import subprocess

def check_working_dir():
    current_dir = os.getcwd()  # Get the current working directory

    if os.path.basename(current_dir) == 'working_dir':
        print("You are in the 'working_dir' directory.")
    else:
        print("You are not in the 'working_dir' directory.")

# Call the function to check
check_working_dir()

extension_name = input("What is the name of the module you are trying to migrate? \n").lower()

# Check if the directory exists
if not os.path.exists(extension_name):
    # If it doesn't exist, create it
    os.makedirs(extension_name)
    print(f"Directory '{extension_name}' created successfully.")
else:
    print(f"Directory '{extension_name}' already exists.")

os.chdir(extension_name)

if not os.path.exists(f"saltext-{extension_name}"):
    command = f'''create-salt-extension -A "EITR Technologies" \
        -E "devops@eitr.tech" \
        -S "Salt Extension for interacting with {extension_name.capitalize()}" \
        -U "https://github.com/salt-extensions/saltext-{extension_name}" \
        -L apache \
        --dest saltext-{extension_name} \
        {extension_name}'''

    # Run the command using subprocess
    subprocess.run(command, shell=True, check=True)
else:
    print(f"Looks like the create-salt-extension command was already ran because the saltext-{extension_name} already exists")


os.chdir(f"saltext-{extension_name}")

current_directory = os.getcwd()

def is_git_initialized(directory_path):
    git_dir = os.path.join(directory_path, '.git')
    return os.path.exists(git_dir)

if is_git_initialized(current_directory):
    print("Git repository is already initialized in this directory.")
else:
    print("Git repository is not initialized in this directory.")
    subprocess.run(['git', 'init'], check=True)

subprocess.run(['git', 'branch', '-m', 'main'], check=True)


### creating the needed files in /requirements ###

# Check if the directory exists
if not os.path.exists("requirements"):
    # If it doesn't exist, create it
    os.makedirs("requirements")
    print(f"Directory requirements created successfully.")
else:
    print(f"Directory requirements already exists.")

os.chdir("requirements")

filenames = ["changelog.txt", "dev.txt", "docs.txt", "docs-auto.txt", "lint.txt", "tests.txt"]

for filename in filenames:
    if not os.path.exists(filename):
        with open(filename, 'w'):
            pass  # Create an empty file if it doesn't exist
        print(f"File '{filename}' created.")
    else:
        print(f"File '{filename}' already exists.")

## Dealing with pre-commits

subprocess.run(['pip', 'install', 'pre-commit'], check=True)

subprocess.run(['pre-commit', 'install'])

subprocess.run(['git', 'add', '.'])

print("*******************************************************************************************")
print("Script is complete. You will now have to do the git committing as that can get complicated")
print("Here is the command to run to do so:")
print("git commit -m 'Initial commit of extension framework'")






